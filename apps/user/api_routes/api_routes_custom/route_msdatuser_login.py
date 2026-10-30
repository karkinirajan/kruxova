# ********************
# imports python
# ********************
# ********************
# imports django
# ********************
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate

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
from apps.user.api_routes import serializers as msdatuser_serializers

# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
request_def = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING, description="username"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="password"),
    },
)
response_def = openapi.Response(
    "response description", msdatuser_serializers.CustomRoutesDefaultSerializerUser
)


@swagger_auto_schema(
    operation_description="POST store a new user",
    methods=["POST"],
    request_body=request_def,
    responses={201: response_def},
)
@api_view(["POST"])
def route(request):

    if request.method == "POST":
        try:
            # ================================
            # PARSE REQUEST
            # ================================
            req_data = JSONParser().parse(request)
            req_username = req_data.get("username")
            req_password = req_data.get("password")
            if not req_username or not req_password:
                return Response(
                    {"error": "username and password are required"}, status.HTTP_400_BAD_REQUEST
                )

            # ================================
            # RUN QUERIES
            # ================================
            # USERS
            user = authenticate(username=req_username, password=req_password)

            # ================================
            # SERIALIZE RESPONSE
            # ================================
            if user:
                serializer_instance = msdatuser_serializers.UserSerializer(user)
                return Response(serializer_instance.data, status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "user not found, confirm username and password"},
                    status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        except ParseError:
            return Response(
                {"error": "request body must be valid JSON"}, status.HTTP_400_BAD_REQUEST
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
