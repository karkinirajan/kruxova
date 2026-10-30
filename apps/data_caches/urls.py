from django.urls import path

from apps.data_caches.api_routes import route_update_all_caches, route_status, route_caches

urlpatterns = [
    # ==================================================
    # CACHES MANAGEMENT ROUTES
    # ==================================================
    path("man/refresh/", route_update_all_caches.route, name="app_datacache_api_route_refresh"),
    path("man/status/", route_status.route, name="app_datacache_api_route_status"),
    # ==================================================
    # GET CACHES ROUTES
    # ==================================================
    path("data/caches/", route_caches.route, name="app_datacache_api_route_caches.route"),
]
