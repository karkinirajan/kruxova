import pytest


def test_count_of_an_empty_dataset(api, db):
    res = api.get("/api/dmi/data/count/")
    assert res.status_code == 200 and res.json() == {"count": 0}


def test_dmi_data_requires_offset_and_limit(api, db):
    res = api.get("/api/dmi/data/all/")  # used to raise MultiValueDictKeyError (HTTP 500)
    assert res.status_code == 400
    assert set(res.json()["error"]) == {"offset", "limit"}


@pytest.mark.parametrize("query", ["offset=x&limit=5", "offset=0&limit=y", "offset=-1&limit=5"])
def test_dmi_data_rejects_non_integer_or_negative_values(api, db, query):
    assert api.get(f"/api/dmi/data/all/?{query}").status_code == 400


def test_dmi_data_returns_a_json_list(api, db):
    # used to raise TypeError: the response helper was called without its status argument
    res = api.get("/api/dmi/data/all/?offset=0&limit=10")
    assert res.status_code == 200 and res.json() == []


def test_latest_data_on_an_empty_database_is_404_not_500(api, db):
    res = api.get("/api/data/latest/")
    assert res.status_code == 404 and "no data" in res.json()["error"]


def test_after_datetime_requires_its_parameter(api, db):
    assert api.get("/api/data/after_datetime/").status_code == 400


# --- subdashboard interests -----------------------------------------------------------------


def test_interest_store_needs_a_token(api, db):
    res = api.post(
        "/api/subdashboard/interest/",
        {"email": "a@example.com", "dashboard": "health"},
        format="json",
    )
    assert res.status_code in (401, 403)


def test_interest_store_show_and_destroy(auth_api, api, db):
    created = auth_api.post(
        "/api/subdashboard/interest/",
        {"email": "a@example.com", "dashboard": "health"},
        format="json",
    )
    assert created.status_code == 201, created.content
    shown = api.get("/api/subdashboard/interests/a@example.com/")
    assert shown.status_code == 200 and shown.json()[0]["dashboard"] == "health"
    assert api.get("/api/subdashboard/interests/nobody@example.com/").status_code == 404
    assert auth_api.delete("/api/subdashboard/interest/a@example.com/").status_code in (200, 204)
    assert api.get("/api/subdashboard/interests/a@example.com/").status_code == 404


def test_interest_store_rejects_invalid_input(auth_api, db):
    res = auth_api.post("/api/subdashboard/interest/", {"email": "a@example.com"}, format="json")
    assert res.status_code == 400
