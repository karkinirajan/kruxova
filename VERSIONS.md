# Versions

Resolved in `uv.lock` on 2026-10-30. "Previous" is the old `requirements.txt`.

| Component | Version | Previous | Note |
|---|---|---|---|
| Python | 3.13 (resolved 3.13.18) | not pinned | `requires-python >=3.13` |
| Django | 5.2.18 | 3.0.2 | 5.2 is the LTS line |
| Django REST Framework | 3.18.3 | 3.11.0 | |
| django-filter | 26.2 | 2.4.0 | |
| django-cors-headers | 4.9.0 | 3.7.0 | 4.x renamed `CORS_ORIGIN_ALLOW_ALL` to `CORS_ALLOW_ALL_ORIGINS`; the old name silently did nothing |
| drf-yasg | 1.21.18 | 1.20.0 | still imports `pkg_resources`, so `setuptools` is a runtime dependency |
| setuptools | 84.2.1 | n/a | see drf-yasg |
| Celery | 5.6.3 | 4.4.7 | `celery[redis]` |
| kombu | 5.6.2 | 4.6.11 | |
| redis (client) | 6.4.0 | n/a | |
| django-celery-results | 2.6.0 | n/a (used in settings, not pinned) | |
| dj-database-url | 3.1.2 | n/a | `DATABASE_URL` |
| psycopg | 3.3.6 (binary) | psycopg2-binary 2.8.6 | |
| WhiteNoise | 6.12.0 | 5.0.1 | |
| pymemcache | 4.0.0 | n/a | only used when `MEMCACHED_LOCATION` is set |
| gunicorn | 26.2.0 | n/a | |
| coreapi, pytz, sqlparse (pinned) | removed | 2.3.3, 2019.3, 0.3.0 | not used by the code; Django 5 brings its own dependencies |
| django-elasticsearch-dsl, elasticsearch, elasticsearch-dsl | removed | 7.2.2, 7.17.0, 7.4.0 | no code imports them |

Dev: pytest 9.2.0, pytest-django 4.14.0, ruff 0.17.3.

`DEVELOPMENT.md` previously claimed Django 6.0.2 on Python 3.14; that never matched the pinned requirements and has been corrected.
