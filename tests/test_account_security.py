import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def admin_api(db):
    admin = get_user_model().objects.create_user(
        "boss", "boss@example.com", "pw-12345-xyz", is_staff=True
    )
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=admin).key}")
    return client


def test_login_response_never_contains_the_password_hash(api, user):
    res = api.post(
        "/api/account/login/", {"username": "analyst", "password": "pw-12345-xyz"}, format="json"
    )
    assert res.status_code == 200
    assert "password" not in res.json() and "pbkdf2" not in res.content.decode()


def test_user_list_is_not_public(api, user):
    # it used to return every user's password hash to anonymous callers
    res = api.get("/api/crud/user/")
    assert res.status_code in (401, 403)
    assert "pbkdf2" not in res.content.decode()


def test_user_list_is_not_open_to_ordinary_token_holders(auth_api, user):
    assert auth_api.get("/api/crud/user/").status_code == 403


def test_a_token_holder_cannot_change_another_users_password(auth_api, db):
    other = get_user_model().objects.create_user("other", "o@example.com", "original-pw-1")
    res = auth_api.patch(f"/api/crud/user/{other.pk}/", {"password": "hijacked"}, format="json")
    assert res.status_code == 403
    other.refresh_from_db()
    assert other.check_password("original-pw-1")


def test_staff_can_list_users_without_password_data(admin_api, user):
    res = admin_api.get("/api/crud/user/")
    assert res.status_code == 200 and len(res.json()) == 2
    assert "password" not in res.content.decode().lower().replace("password_", "")


def test_staff_created_users_get_a_hashed_password(admin_api, db):
    res = admin_api.post(
        "/api/crud/user/",
        {"username": "new", "email": "n@example.com", "password": "fresh-pw-123"},
        format="json",
    )
    assert res.status_code == 201 and "password" not in res.json()
    created = get_user_model().objects.get(username="new")
    assert created.password != "fresh-pw-123" and created.check_password("fresh-pw-123")


def test_staff_password_updates_are_hashed(admin_api, user):
    res = admin_api.patch(f"/api/crud/user/{user.pk}/", {"password": "rotated-pw-9"}, format="json")
    assert res.status_code == 200
    user.refresh_from_db()
    assert user.password != "rotated-pw-9" and user.check_password("rotated-pw-9")
