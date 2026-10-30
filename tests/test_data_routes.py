from urllib.parse import quote


from apps.main import models as m


def test_the_shipped_fixtures_load(reference_data):
    # they used to name their models "apps.main.X", which Django cannot resolve
    assert m.Location.objects.count() == 925
    assert m.LocationHierarchyLevel.objects.count() == 5
    assert m.Datasource.objects.count() == 17
    assert m.Indicator.objects.count() == 33


def test_reference_data_is_served(api, reference_data):
    assert len(api.get("/api/crud/location/").json()) == 925
    assert len(api.get("/api/crud/datasources/").json()) == 17


def test_count_and_latest(api, data_rows):
    assert api.get("/api/dmi/data/count/").json() == {"count": 3}
    assert api.get("/api/data/latest/").status_code == 200


def test_dmi_data_slices_by_offset_and_limit(api, data_rows):
    # `limit` is the end index of the slice, as it always was
    assert len(api.get("/api/dmi/data/all/?offset=0&limit=2").json()) == 2
    assert len(api.get("/api/dmi/data/all/?offset=1&limit=3").json()) == 2
    assert api.get("/api/dmi/data/all/?offset=5&limit=9").json() == []


def test_data_by_location_level_and_period(api, data_rows):
    level = data_rows[0].location.level_id
    everything = api.get(f"/api/data/location_level/{level}")
    assert everything.status_code == 200
    only_2019 = api.get(f"/api/data/location_level/{level}?period=2019")
    assert only_2019.status_code == 200
    assert len(only_2019.json()) <= len(everything.json())


def test_data_after_a_datetime(api, data_rows):
    past = api.get("/api/data/after_datetime/?datetime=" + quote("2000-01-01 00:00:00"))
    assert past.status_code == 200 and len(past.json()["created"]) == 3
    future = api.get("/api/data/after_datetime/?datetime=" + quote("2999-01-01 00:00:00"))
    assert future.status_code == 200 and future.json() == {"created": [], "updated": []}


def test_after_datetime_rejects_a_bad_format(api, db):
    res = api.get("/api/data/after_datetime/?datetime=yesterday")
    assert res.status_code == 400 and "error" in res.json()


def test_saving_data_links_the_datasource_to_the_indicator(data_rows):
    row = data_rows[0]
    assert row.datasource in row.indicator.datasources.all()
