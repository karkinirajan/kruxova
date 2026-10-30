"""Settings for the test suite: debug on, in-memory DB, eager Celery, temp media."""

import os
import tempfile

os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-secret-key")
os.environ.setdefault("DJANGO_DEBUG", "true")
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")
os.environ.pop("MEMCACHED_LOCATION", None)

from core.settings.base import *  # noqa: E402,F401,F403

ALLOWED_HOSTS = ["testserver", "localhost"]
MEDIA_ROOT = tempfile.mkdtemp(prefix="msdat-media-")
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
MIDDLEWARE = [m for m in MIDDLEWARE if "whitenoise" not in m]  # noqa: F405
CELERY_TASK_ALWAYS_EAGER = True
