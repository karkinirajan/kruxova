from django.urls import path

from apps.subdashboard.api_routes import (
    route_interests_destroy,
    route_interests_index,
    route_interests_show,
    route_interests_store,
)

urlpatterns = [
    path("interests/", route_interests_index.route, name="app_subdashoard_route_interests_index"),
    path("interest/", route_interests_store.route, name="app_subdashoard_route_interests_store"),
    path(
        "interest/<email>/",
        route_interests_destroy.route,
        name="app_subdashoard_route_interests_destroy",
    ),
    path(
        "interests/<email>/",
        route_interests_show.route,
        name="app_subdashoard_route_interests_show",
    ),
]
