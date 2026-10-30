import pytest

from apps.main.models import Group


def test_reads_are_public(api, db):
    res = api.get("/api/crud/group/")
    assert res.status_code == 200
    assert res.json() == []


def test_writes_need_a_token(api, db):
    res = api.post("/api/crud/group/", {"name": "Health", "decription": "x"}, format="json")
    assert res.status_code in (401, 403)
    assert Group.objects.count() == 0


def test_create_read_update_delete_with_a_token(auth_api, db):
    created = auth_api.post(
        "/api/crud/group/", {"name": "Health", "decription": "d"}, format="json"
    )
    assert created.status_code == 201
    pk = created.json()["id"]
    assert auth_api.get(f"/api/crud/group/{pk}/").json()["name"] == "Health"
    patched = auth_api.patch(f"/api/crud/group/{pk}/", {"name": "Education"}, format="json")
    assert patched.status_code == 200 and Group.objects.get(pk=pk).name == "Education"
    assert auth_api.delete(f"/api/crud/group/{pk}/").status_code == 204
    assert Group.objects.count() == 0


def test_validation_errors_are_400(auth_api, db):
    res = auth_api.post("/api/crud/group/", {"name": "only a name"}, format="json")
    assert res.status_code == 400 and "decription" in res.json()


def test_an_invalid_token_is_rejected_even_for_reads(api, db):
    api.credentials(HTTP_AUTHORIZATION="Token not-a-real-token")
    assert api.get("/api/crud/group/").status_code == 401


@pytest.mark.parametrize(
    "resource",
    ["group", "location", "location_hierarchy_level", "valuetypes", "factors", "datasources"],
)
def test_main_resources_list_publicly(api, db, resource):
    assert api.get(f"/api/crud/{resource}/").status_code == 200


# --- login ---------------------------------------------------------------------------------


def test_login_with_valid_credentials(api, user):
    res = api.post(
        "/api/account/login/", {"username": "analyst", "password": "pw-12345-xyz"}, format="json"
    )
    assert res.status_code == 200 and res.json()["username"] == "analyst"


def test_login_with_wrong_password_is_422(api, user):
    res = api.post("/api/account/login/", {"username": "analyst", "password": "no"}, format="json")
    assert res.status_code == 422


@pytest.mark.parametrize("body", [{}, {"username": "analyst"}, {"password": "x"}, {"username": ""}])
def test_login_with_missing_fields_is_400_not_500(api, user, body):
    assert api.post("/api/account/login/", body, format="json").status_code == 400


def test_login_with_a_malformed_body_is_400(api, user):
    res = api.post("/api/account/login/", "{not json", content_type="application/json")
    assert res.status_code == 400


def test_login_is_post_only(api, db):
    assert api.get("/api/account/login/").status_code == 405
