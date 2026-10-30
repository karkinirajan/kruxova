# ********************
# imports python
# ********************
import json

# ********************
# imports django
# ********************
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# **********************
# imports third-party
# **********************
from drf_yasg.utils import swagger_auto_schema

# ********************
# imports shared
# ********************
from shared.legacy_converters import convert_lga


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(operation_description="GET data by states-lga with period", methods=["GET"])
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):
    if request.method == "GET":
        response_data = convert_lga.run_process()

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
