from django.urls import path

from apps.legacy.api_routes import (
    route_meta_data_test,
    route_datasource_meta_test,
    route_indicator_meta_data_test,
)

urlpatterns = [
    # path(
    #    'estimates/',
    #    route_estimates.route,
    #    name='apps.legacy_api_route_legacy_estimates'
    # ),
    # path(
    #    'lga/',
    #    route_lga_data.route,
    #    name='apps.legacy_api_route_legacy_lga'
    # ),
    # path(
    #    'master_sheet/',
    #    route_master_sheet.route,
    #    name='apps.legacy_api_route_master_sheet.route'
    # ),
    path(
        "meta_data_test/",
        route_meta_data_test.route,
        name="apps.legacy_api_route_legacy_meta_data_test",
    ),
    path(
        "datasource_meta_data_test/",
        route_datasource_meta_test.route,
        name="apps.legacy_api_route_datasource_meta_test.route",
    ),
    path(
        "inidicator_meta_data_test/",
        route_indicator_meta_data_test.route,
        name="apps.legacy_api_route_indicator_meta_data_test.route",
    ),
]
