import json

import pytest

from apps.event_trail.middleware import SAFE_META_KEYS, safe_meta
from apps.event_trail.models import TrailRequest


def test_safe_meta_drops_credentials_and_the_wsgi_environment():
    meta = {
        "REMOTE_ADDR": "203.0.113.9",
        "HTTP_USER_AGENT": "pytest",
        "HTTP_AUTHORIZATION": "Token super-secret",
        "HTTP_COOKIE": "sessionid=abc",
        "wsgi.input": object(),
        "SECRET_KEY": "x",
    }
    kept = safe_meta(meta)
    assert kept == {"REMOTE_ADDR": "203.0.113.9", "HTTP_USER_AGENT": "pytest"}
    assert set(kept) <= set(SAFE_META_KEYS)


@pytest.mark.django_db
def test_a_mutating_authenticated_request_is_recorded_without_the_token(auth_api):
    res = auth_api.post("/api/crud/group/", {"name": "Audit", "decription": "d"}, format="json")
    assert res.status_code == 201
    trail = TrailRequest.objects.get()
    assert trail.method == "POST"
    request = json.loads(trail.request)
    assert request["route"] == "/api/crud/group/" and request["method"] == "POST"
    assert json.loads(trail.response) == {"status_code": 201}
    assert "Token " not in trail.request and "HTTP_AUTHORIZATION" not in trail.request


@pytest.mark.django_db
def test_form_posts_record_field_names_but_never_values(auth_api):
    auth_api.post(
        "/api/crud/group/",
        {"name": "visible-name", "decription": "hunter2-secret"},
        format="multipart",
    )
    trail = TrailRequest.objects.get()
    request = json.loads(trail.request)
    assert request["form_fields"] == ["decription", "name"]
    assert "hunter2-secret" not in trail.request and "visible-name" not in trail.request


@pytest.mark.django_db
def test_reads_and_anonymous_requests_are_not_recorded(api, auth_api):
    api.get("/api/crud/group/")
    auth_api.get("/api/crud/group/")
    assert TrailRequest.objects.count() == 0
