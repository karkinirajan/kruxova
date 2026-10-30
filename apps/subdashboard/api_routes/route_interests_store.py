# ********************
# imports python
# ********************
# ********************
# imports django
# ********************
from rest_framework import status
from rest_framework.parsers import JSONParser
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
from apps.subdashboard.api_routes import serializers as serializers_custom

# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
response_def = openapi.Response(
    "response description", serializers_custom.CustomRoutesDefaultSerializerInterest
)


@swagger_auto_schema(
    operation_description="POST store a new subdashboard interests",
    methods=["POST"],
    request_body=serializers_custom.CustomRoutesDefaultSerializerInterest,
    responses={201: response_def},
)
@api_view(["POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):

    if request.method == "POST":
        try:
            # ================================
            # PARSE REQUEST
            # ================================
            req_data = JSONParser().parse(request)

            # ================================
            # RUN QUERIES
            # ================================
            serializer_instance = serializers_custom.CustomRoutesDefaultSerializerInterest(
                data=req_data
            )
            if serializer_instance.is_valid():
                serializer_instance.save()
            else:
                return Response({"message": "input validation failed"}, status.HTTP_400_BAD_REQUEST)

            # ================================
            # SERIALIZE RESPONSE
            # ================================
            return Response(serializer_instance.data, status.HTTP_201_CREATED)

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
