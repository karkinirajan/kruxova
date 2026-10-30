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
req_param_path_offset = openapi.Parameter(
    "offset", openapi.IN_QUERY, description="query offset", type=openapi.TYPE_INTEGER
)

req_param_path_limit = openapi.Parameter(
    "limit", openapi.IN_QUERY, description="query limit", type=openapi.TYPE_INTEGER
)


class RequestSerializer(serializers.Serializer):
    offset = serializers.IntegerField(min_value=0)
    limit = serializers.IntegerField(min_value=0)

    class Meta:
        ref_name = "apps.main_get_data_request"


class Response200Serializer(serializers.Serializer):
    data = {}

    class Meta:
        ref_name = "apps.main_get_data_response200"


# respose http 400 definition
class Response400Serializer(serializers.Serializer):
    error = serializers.CharField()

    class Meta:
        ref_name = "apps.main_get_data_response400"


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(
    operation_description="GET action to pull data in dmi format",
    methods=["GET"],
    manual_parameters=[req_param_path_offset, req_param_path_limit],
    responses={
        200: openapi.Response("response description", Response200Serializer),
        400: openapi.Response("response description", Response400Serializer),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):
    if request.method == "GET":
        serializer_req = RequestSerializer(data=request.GET)
        if serializer_req.is_valid():
            offset = serializer_req.validated_data["offset"]
            limit = serializer_req.validated_data["limit"]
            # NOTE: unchanged behaviour - `limit` is the end index of the slice, not a page size.
            queryset = main_models.Data.objects.all()[offset:limit]
            return utils_drf.helper_json_response(
                Response200Serializer, queryset.values(), status.HTTP_200_OK
            )
        return utils_drf.helper_json_response(
            Response400Serializer,
            {"error": serializer_req.errors},
            status.HTTP_400_BAD_REQUEST,
        )
    return utils_drf.helper_json_response(
        Response400Serializer, {"error": "bad request"}, status.HTTP_400_BAD_REQUEST
    )
