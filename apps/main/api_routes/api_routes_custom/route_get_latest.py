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
# CUSTOM RESPONSE SERIALIZER DEFINITION
# ******************************************


# respose http 200 definition
class Response200Serializer(serializers.Serializer):
    data = {}

    class Meta:
        ref_name = "apps.main_get_last_update_response200"


# respose http 400 definition
class Response400Serializer(serializers.Serializer):
    error = serializers.CharField()

    class Meta:
        ref_name = "apps.main_get_last_update_response400"


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(
    operation_description="GET action to get the datetime of the last updated data row",
    methods=["GET"],
    responses={
        200: openapi.Response("response description", Response200Serializer),
        400: openapi.Response("response description", Response400Serializer),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):

    if request.method == "GET":
        queryset = main_models.Data.objects.order_by("updated_at").last()

        if queryset is None:  # no data loaded yet
            return utils_drf.helper_json_response(
                Response400Serializer, {"error": "no data available yet"}, status.HTTP_404_NOT_FOUND
            )

        # SERIALIZE AND RETURN
        return utils_drf.helper_json_response(
            Response200Serializer, queryset.created_at, status.HTTP_200_OK
        )

    else:
        # SERIALIZE AND RETURN
        return utils_drf.helper_json_response(
            Response400Serializer, {"error": "bad request"}, status.HTTP_400_BAD_REQUEST
        )
