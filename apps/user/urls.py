# *****************************************
# IMPORTs django
# *****************************************
from django.urls import path, include
from rest_framework import routers

# *****************************************
# IMPORTs app
# *****************************************
from apps.user.api_routes.api_routes_crud import (
    api_routes_crud_registry as user_api_routes_crud_registry,
)
from apps.user.api_routes.api_routes_custom import route_msdatuser_login

api_router_user = routers.DefaultRouter()
user_api_routes_crud_registry.register_routes(api_router_user)

urlpatterns = [
    path("account/", include(api_router_user.urls)),
    path("account/login/", route_msdatuser_login.route, name="apps.user_route_msdatuser_login"),
]
