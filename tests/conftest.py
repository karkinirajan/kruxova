import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("analyst", "analyst@example.com", "pw-12345-xyz")


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def auth_api(user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=user)[0].key}")
    return client


FIXTURES = [
    "fixture_1_value_type",
    "fixture_1_factor",
    "fixture_1_datasource",
    "fixture_1_location_hierarchy_level",
    "fixture_2_indicator",
    "fixture_2_location",
    "fixture_3_datasource_specific_indicator",
    "fixture_3_link",
]


@pytest.fixture
def reference_data(db):
    """The shipped reference data: value types, factors, datasources, 925 locations, ..."""
    from django.core.management import call_command

    call_command("loaddata", *FIXTURES, verbosity=0)


@pytest.fixture
def data_rows(reference_data):
    from apps.main import models as m

    indicator = m.Indicator.objects.first()
    datasource = m.Datasource.objects.first()
    value_type = m.ValueType.objects.first()
    locations = list(m.Location.objects.all()[:3])
    return [
        m.Data.objects.create(
            indicator=indicator,
            period=period,
            location=location,
            datasource=datasource,
            value_type=value_type,
            value=str(i),
        )
        for i, (location, period) in enumerate(zip(locations, ["2018", "2018", "2019"]))
    ]
