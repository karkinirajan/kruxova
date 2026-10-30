"""msdat-python-api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include

# *****************************************
# IMPORTs shared
# *****************************************
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ***********************************
# DJANGO ADMIN custom
# ***********************************
admin.site.site_header = "MSDAT API (CARD schema v1.2.0)"
admin.site.site_title = "MSDAT python api"
admin.site.index_title = "Management interface"

# *****************************************
# REGISTER DRF_YASG schema doc
# *****************************************
schema_view = get_schema_view(
    openapi.Info(
        title="MSDAT API (CARD schema v1.2.0)",
        default_version="v1",
        description="""WEB-GUI DOCUMENTATION with swagger(OPENApi),
      Note!! all (POST,PATCH,DELETE,PUT) routes are token protected
      For clients to authenticate use the provided tokens,
      the token key should be included in the Authorization HTTP header.
      The key should be prefixed by the string literal "Token",
      with whitespace separating the two strings.
      For example: Authorization: Token <your-token>
      Example:
      curl -X GET http://127.0.0.1:8000/api/example/
      -H 'Authorization: Token <your-token>' """,
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # REGISTER DRF_YASG schema doc
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(
        "apidoc/swag/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="apidoc-swag",
    ),
    path(
        "apidoc/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    # REGISTER ADMIN
    path("youWouldNEVERHAVEguessedThiswasTHEadminurl/", admin.site.urls),
    # REGISTER APPs/APIs
    path("api/", include("apps.main.urls")),
    path("api/caches/", include("apps.data_caches.urls")),
    path("api/legacy/", include("apps.legacy.urls")),
    path("api/dmi/", include("apps.dmi.urls")),
    path("api/", include("apps.user.urls")),
    path("api/subdashboard/", include("apps.subdashboard.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
