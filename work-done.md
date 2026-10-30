# Work done: kruxova

Branch: `chore/modernize` (local, not pushed). Date: 2026-10-30.

## What was there
A Django 3.0 / DRF API (apps `main`, `dmi`, `data_caches`, `event_trail`, `user`, `subdashboard`, `legacy`) for MSDAT with 2020 pins. The tree held two copies of the code: the live `apps/`, `shared/`, `core/` and a superseded 2022 copy (`app_*`, `libs`, `msdat-python-api`, `msdat_python_api_settings`) that differed only by import renames. There was no `manage.py` (it was in `.gitignore`), and `core/settings/__init__.py` imported a git-ignored `local.py`, so a fresh clone could not start. Settings were split into per-environment files that hardcoded the same database password, a Django secret key, `ALLOWED_HOSTS=['*']` and CORS open to everyone. No tests, no CI.

## Changes by file
| Path | Before | Change |
|---|---|---|
| `app_main`, `app_legacy`, `app_user`, `app_subdashboard`, `app_dmi`, `app_data_caches`, `app_event_trail`, `libs`, `msdat-python-api`, `msdat_python_api_settings` (120 files) | superseded duplicate of `apps/`, `shared/`, `core/` | Deleted after diffing: only import renames (`app_main` to `apps.main`, `libs` to `shared`) differed |
| `core/settings/local_pgsql.py`, `staging.py`, `production.py` | hardcoded database password per environment | Deleted. One env-driven module replaces them |
| `core/settings/utils.py`, `script_bash_mark_as_{local,staging,production}.sh` | `E4E_ENVVAR_MSDATAPI_ENV` environment switch | Deleted; nothing else read the switch |
| `core/settings/__init__.py` | imported git-ignored `local.py` | Re-exports `base` |
| `core/settings/base.py` | hardcoded secret key, `ALLOWED_HOSTS=['*']`, `CORS_ORIGIN_ALLOW_ALL` (ignored by cors-headers 4), Elasticsearch block, memcached host constants | Env-driven: secret key (fails fast unless `DJANGO_DEBUG=true`), hosts, CSRF origins, `DATABASE_URL`, CORS, Celery broker, optional memcached with a LocMem fallback, WhiteNoise `STORAGES`, HTTPS/HSTS/secure cookies when not debug |
| `core/settings_test.py` | absent | New test settings (in-memory SQLite or `TEST_DATABASE_URL`, eager Celery, temp media) |
| `manage.py`, `.gitignore` | `manage.py` and `local.py` were ignored | `manage.py` added and tracked; `.python-version` un-ignored; `.venv`, `.env`, caches ignored |
| `pyproject.toml`, `uv.lock`, `.python-version`, `requirements.txt` | pins from 2020 (Django 3.0.2) | uv project on Python 3.13, Django 5.2 LTS; `requirements.txt` regenerated from the lock |
| `apps/data_caches/api_routes/route_update_all_caches.py` | HTTP 500 when the Celery broker is down | `503 {"status": "BROKER_UNAVAILABLE"}` |
| `apps/main/.../route_get_latest.py` | `AttributeError` (500) on an empty database | 404 `{"error": "no data available yet"}` |
| `apps/dmi/.../route_get_data.py` | missing `offset`/`limit` raised `MultiValueDictKeyError` (500); the response helper was called without its status argument (500 on any valid request) | Validates integers (>= 0), 400 on bad input, correct status codes. Slice semantics unchanged (`limit` is the end index) |
| `apps/user/.../route_msdatuser_login.py` | missing fields or a malformed body returned 500 | 400 with a message |
| `apps/event_trail/middleware.py` | stored all of `request.META` (including the `Authorization` token and cookies) in the database, and a `query_params` value that was the text of an iterator object | Stores only a safe subset of headers and the names of submitted form fields (never values) |
| `apps/main/.../api_routes_crud_serializers.py`, `api_routes_crud_viewsets.py` (`UserViewSet`, served at `/api/crud/user/`) | anonymous `GET` returned every Django user including the stored password hash; `POST`/`PATCH` stored the password as clear text; any token holder could overwrite another user's password | `password` is write-only and hashed on create/update; the endpoint is staff-only (`IsAdminUser`) |
| `apps/user/api_routes/serializers.py` (`UserSerializer`) | the login response included the password hash | `password` is write-only |
| `apps/user/models.py` | `User.__str__` referenced a nonexistent `user_id` | Uses `id` |
| `apps/main/fixtures/*.json` (8 files) | model labels `apps.main.X`; Django could not load any of them | Labels changed to `main.X`; all 1,015 objects load |
| `core/urls.py` | API docs example contained what looks like a real API token | Replaced with `<your-token>` |
| 14 route modules | `from rest_framework.schemas import ManualSchema` (gone in the installed DRF 3.18.3, so the import failed), unused | Import removed |
| `script_start_celery.sh` | `celery -A msdat-python-api` (invalid module name) | `celery -A core` |
| all other `.py` files | mixed formatting, about 137 unused imports | `ruff check --fix` and `ruff format`; bare `except:` became `except Exception:`; `== None` became `is None` |
| `tests/` (6 modules, `conftest.py`) | none | 56 tests |
| `.github/workflows/ci.yml` | absent | Lint, format, migration drift and tests on SQLite, plus the suite on PostgreSQL 17 |
| `.env.example` | absent | Demo values for every variable |
| `README.md`, `DEVELOPMENT.md`, `CHANGELOG.md`, `VERSIONS.md`, `work-done.md` | README generic; DEVELOPMENT.md claimed Django 6 / Python 3.14 and the removed env switch | README rewritten to match the code; DEVELOPMENT.md corrected; changelog entry; versions and this file added |
| `.DS_Store`, `.output.txt`, `__pycache__` | tracked | Removed from git |

## Verification (actual runs)
- `uv run pytest -q`: 56 passed on in-memory SQLite (the 49 tests that existed before the account-security fix also passed on PostgreSQL 17; the 7 added afterwards were not re-run there) (psycopg 3, throwaway container, removed afterwards).
- `uv run ruff check .` and `ruff format --check .`: clean. One scoped relaxation, stated here on purpose: `E501` (line length) is ignored for `shared/legacy_converters/*`, which are lookup tables of indicator names a character or two over 100.
- `makemigrations --check --dry-run`: no changes. `migrate` applies cleanly to a fresh SQLite and a fresh PostgreSQL database.
- `script_load_data.sh` loads all 1,015 fixture objects on PostgreSQL.
- `check --deploy` with production-style environment: only the two optional HSTS warnings (include-subdomains, preload). Without `DJANGO_SECRET_KEY` and `DJANGO_DEBUG` the app refuses to start.
- `celery -A core report` imports the app; `collectstatic --dry-run` resolves 193 files.
- Not run: a Celery worker against a real Redis, memcached, and a production-sized data set. The refresh task is tested with the broker mocked.

## Needs your attention
- **Treat user passwords as exposed.** Before this change anyone could read `/api/crud/user/` and get every account's password hash. On any deployed instance, force password resets and rotate tokens.
- **Rotate secrets.** The database password (the same one in three settings files), the Django secret key and the API token that was in the docs example are in git history. Removing them from the working tree does not remove them from history. Revoke that token.
- **No `LICENSE` file.** The old README claimed MIT. I did not add a license on someone else's behalf; the README now says to add one.
- Left alone, flagged only:
  - `/api/crud/...` for the MSDAT `User` and `Contact` tables (`apps/user`) is still publicly readable and includes email addresses (no password data); restrict it if that is personal data you hold.
  - Many route handlers return `str(exception)` to the client on a 500, which can leak internals. This is the repo's pattern across dozens of routes.
  - `CORS_ALLOW_ALL_ORIGINS` defaults to true when no origins are listed (as before); set `CORS_ALLOWED_ORIGINS` for production.
  - The `Data` slice endpoint treats `limit` as an end index, not a page size (kept for compatibility).
  - `apps/legacy` and `shared/legacy_converters` contain large hand-written mapping tables; they are formatted but not covered by tests.
- Nothing pushed. To publish: `git push -u origin chore/modernize`
