# *****************************************
# IMPORTs django
# *****************************************
from django.urls import path

# *****************************************
# IMPORTs app
# *****************************************
from apps.dmi.api_routes.api_routes_custom import route_get_count, route_get_data

urlpatterns = [
    # *****************************************
    # ROUTES crud(default) api routes
    # *****************************************
    # *****************************************
    # ROUTES custom api definitions
    # *****************************************
    path("data/count/", route_get_count.route, name="apps.dmi_api_route_get_count"),
    path("data/all/", route_get_data.route, name="apps.dmi_api_route_get_data"),
]
