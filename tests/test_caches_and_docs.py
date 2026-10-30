from unittest import mock

import pytest

from apps.data_caches.models import CHOICES_STATUS_INPROGRESS, DataCacheStatus


def test_refresh_reports_a_missing_broker_as_503(api, db):
    # no Redis in the test run: queueing the task must fail cleanly, not with a 500
    with mock.patch("apps.data_caches.tasks.task_update_data_caches.apply_async") as queued:
        from kombu.exceptions import OperationalError

        queued.side_effect = OperationalError("connection refused")
        res = api.get("/api/caches/man/refresh/")
    assert res.status_code == 503 and res.json() == {"status": "BROKER_UNAVAILABLE"}


def test_refresh_starts_the_task_when_the_broker_is_up(api, db):
    with mock.patch("apps.data_caches.tasks.task_update_data_caches.apply_async") as queued:
        res = api.get("/api/caches/man/refresh/")
    assert res.json() == {"status": "STARTED"}
    queued.assert_called_once()


def test_refresh_is_skipped_while_a_cache_is_in_progress(api, db):
    DataCacheStatus.objects.create(
        cache_name="all_data", cache_type="FILE", status=CHOICES_STATUS_INPROGRESS
    )
    with mock.patch("apps.data_caches.tasks.task_update_data_caches.apply_async") as queued:
        res = api.get("/api/caches/man/refresh/")
    assert res.json() == {"status": "ALREADY_INPROGRESS"}
    queued.assert_not_called()


@pytest.mark.parametrize("path", ["/", "/apidoc/swag/", "/apidoc/redoc/", "/swagger.json"])
def test_api_documentation_renders(api, db, path):
    res = api.get(path)
    assert res.status_code == 200, (path, res.status_code)
