# ********************
# imports python
# ********************

# **********************
# imports third-party
# **********************
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status

# ********************
# imports django
# ********************
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# ********************
# imports app
# ********************
# utils
from shared.utils import utils_drf

# models
from apps.main import models as main_models

# ******************************************
# CUSTOM REQUEST DEFINITION
# ******************************************
req_param_path_id = openapi.Parameter(
    "id", openapi.IN_PATH, description="location level id", type=openapi.TYPE_INTEGER
)

req_param_query_period = openapi.Parameter(
    "period", openapi.IN_QUERY, description="filter by period", type=openapi.TYPE_STRING
)

# ******************************************
# CUSTOM RESPONSE SERIALIZER DEFINITION
# ******************************************


# respose http 200 definition
class Response200Serializer(serializers.Serializer):
    data = {}

    class Meta:
        ref_name = "apps.main_get_by_location_level_response200"


# respose http 400 definition
class Response400Serializer(serializers.Serializer):
    error = serializers.CharField()

    class Meta:
        ref_name = "apps.main_get_by_location_level_response400"


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(
    operation_description="GET action to pull data by location level",
    methods=["GET"],
    manual_parameters=[req_param_path_id, req_param_query_period],
    responses={
        200: openapi.Response("response description", Response200Serializer),
        400: openapi.Response("response description", Response400Serializer),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request, id):

    if request.method == "GET":
        req_param_period = request.GET.get("period", "")

        queryset = None

        if req_param_period == "":
            queryset = main_models.Data.objects.filter(location__level__id=id).select_related()
        else:
            queryset = main_models.Data.objects.filter(
                location__level__id=id, period=req_param_period
            ).select_related()

        # SERIALIZE AND RETURN
        return utils_drf.helper_json_response(
            Response200Serializer, queryset.values(), status.HTTP_200_OK
        )

    else:
        # SERIALIZE AND RETURN
        return utils_drf.helper_json_response(
            Response400Serializer, {"error": "bad request"}, status.HTTP_400_BAD_REQUEST
        )
