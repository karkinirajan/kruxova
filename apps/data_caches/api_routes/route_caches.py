# ********************
# imports python
# ********************
import json

# **********************
# imports third-party
# **********************
from drf_yasg.utils import swagger_auto_schema

# ********************
# imports django
# ********************
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# ********************
# imports app
# ********************
# models
from apps.data_caches import models


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(operation_description="GET the url to data cache files", methods=["GET"])
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):
    if request.method == "GET":
        caches_links = {}

        for cache_name in models.CACHE_NAMES:
            caches_links[cache_name] = "{}{}.json".format(settings.MEDIA_URL, cache_name)

        response_data = caches_links

        # ================================
        # SERIALIZE RESPONSE
        # ================================
        data_serialized = json.dumps(response_data)
        return HttpResponse(data_serialized, content_type="application/json")
    else:
        # ================================
        # SERIALIZE RESPONSE
        # ================================
        data_serialized = json.dumps([])
        return HttpResponse(data_serialized, content_type="application/json")
