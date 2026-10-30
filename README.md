# Kruxova (MSDAT API)

REST API for **MSDAT**, a multi-sectoral data analytics tool. It stores indicators, locations, data sources and the data values that connect them (the CARD schema), serves them to dashboards as JSON, caches the heavy queries as files, and keeps an audit trail of every authenticated change.

## Features

- CRUD API for groups, locations, location hierarchy levels, value types, factors, data sources and indicators. Reads are public, writes need a token; user accounts (`/api/crud/user/`) are staff-only.
- Data endpoints: latest update time, data created/updated after a time, data by location level (optionally by period), and a paged "DMI" export with a count.
- File caches of the large data sets, refreshed by a Celery task (`/api/caches/man/refresh/`, status at `/api/caches/man/status/`).
- Subdashboard "interests" (email and dashboard subscriptions) and a contact/user model.
- Audit trail of authenticated `POST`/`PUT`/`PATCH`/`DELETE` requests, recording route, method, a safe subset of headers, form field names and response status (never the token, cookies or field values).
- Swagger UI at `/` and `/apidoc/swag/`, ReDoc at `/apidoc/redoc/`, schema at `/swagger.json`.
- Legacy converters in `shared/legacy_converters/` that reshape the old MSDAT master sheet, LGA and estimates data.

## Stack

Python 3.13, Django 5.2 LTS, Django REST Framework 3.18, Celery 5.6 (Redis broker), drf-yasg, django-filter, django-cors-headers, WhiteNoise, gunicorn; SQLite by default or PostgreSQL via `DATABASE_URL`. Exact versions: [VERSIONS.md](./VERSIONS.md). Longer background and the data model: [DEVELOPMENT.md](./DEVELOPMENT.md).

## Quickstart

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone <this repo> && cd kruxova
uv sync --frozen
export DJANGO_DEBUG=true            # local work only; uses a dev secret key and SQLite
uv run python manage.py migrate
uv run bash script_load_data.sh     # reference data: 925 locations, indicators, data sources, ...
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Open http://127.0.0.1:8000/ for the Swagger UI. To call the write endpoints, create a token for a user (`uv run python manage.py drf_create_token <username>`) and send `Authorization: Token <your-token>`.

The cache refresh needs a worker: `./script_start_celery.sh` (and Redis at `CELERY_BROKER_URL`). Without a broker the refresh endpoint answers `503 {"status": "BROKER_UNAVAILABLE"}` instead of failing.

## Configuration

The app reads real environment variables (it does not load `.env` itself); `.env.example` lists every name with demo values.

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | required unless `DJANGO_DEBUG=true` | startup fails without it in production |
| `DJANGO_DEBUG` | `false` | debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | comma-separated hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | empty | comma-separated origins |
| `DATABASE_URL` | SQLite file `db.sqlite3` | any dj-database-url URL |
| `CORS_ALLOWED_ORIGINS` / `CORS_ALLOW_ALL_ORIGINS` | allow all when no origins listed | restrict browser origins |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery broker |
| `MEMCACHED_LOCATION` | unset (in-process cache) | memcached for Django's cache |
| `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_HSTS_SECONDS` | `true`, `3600` | used when `DJANGO_DEBUG=false` |

When `DJANGO_DEBUG=false` the app enables the HTTPS redirect, secure cookies and HSTS, and trusts `X-Forwarded-Proto` from the proxy.

## Testing

```bash
uv run pytest -q
uv run ruff check . && uv run ruff format --check .
```

56 tests cover authentication and permissions, account security (no password data is ever returned, user management is staff-only), CRUD, login, the data routes against the shipped fixtures, the cache refresh (with the broker mocked), the audit trail and the API docs. They use `core.settings_test` (in-memory SQLite, eager Celery, temporary media). To run on PostgreSQL: `TEST_DATABASE_URL=postgres://user:pass@localhost:5432/db uv run pytest -q`. CI runs both: `.github/workflows/ci.yml`.

## Project structure

```
core/                 settings (one env-driven module), urls, celery, wsgi/asgi, settings_test
apps/main/            indicators, locations, data, CRUD + custom data routes, fixtures, management command
apps/dmi/             paged data export and count
apps/data_caches/     cache status model, refresh task and routes
apps/event_trail/     audit-trail middleware and model
apps/user/            users, contacts, login route
apps/subdashboard/    dashboard interests
apps/legacy/          adapters for the old MSDAT data structures
shared/               data caching, legacy converters, logging and DRF helpers
tests/                pytest suite
```

## Deployment

Run `gunicorn core.wsgi:application` behind a reverse proxy, with a Celery worker (`./script_start_celery.sh`). Set the production variables above, then `python manage.py migrate` and `python manage.py collectstatic --noinput`. Django's own check passes with a production-style environment apart from two optional HSTS warnings (include-subdomains, preload).

## License

The original README stated MIT, but the repository has no `LICENSE` file. Add one before publishing.
