# ********************
# imports python
# ********************
# ********************
# imports django
# ********************
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# **********************
# imports third-party
# **********************
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# ********************
# imports shared
# ********************
from shared.utils import utils_logger

# ********************
# imports app
# ********************
from apps.subdashboard import models as subdashboard_models
from apps.subdashboard.api_routes import serializers as serializers_custom

# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
user_response = openapi.Response(
    "response description", serializers_custom.CustomRoutesDefaultSerializerInterest
)


@swagger_auto_schema(
    operation_description="GET subdashboard intererests of a user",
    methods=["GET"],
    responses={200: user_response},
)
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request, email):

    if request.method == "GET":
        try:
            # ================================
            # RUN QUERIES
            # ================================

            # USERS
            response_data = subdashboard_models.Interest.objects.filter(email=email)

            # ================================
            # SERIALIZE RESPONSE
            # ================================
            if len(response_data) != 0:
                serializer_instance = serializers_custom.CustomRoutesDefaultSerializerInterest(
                    response_data, many=True
                )
                return Response(serializer_instance.data, status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "user subdashboard interests not found"}, status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            # LOG
            utils_logger.log_print("", str(e), param_oneline=True)

            # ================================
            # SERIALIZE RESPONSE
            # ================================
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # ================================
        # SERIALIZE RESPONSE
        # ================================
        return Response({"message": ""}, status.HTTP_405_METHOD_NOT_ALLOWED)
