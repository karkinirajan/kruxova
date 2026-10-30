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
from drf_yasg.utils import swagger_auto_schema

# ********************
# imports shared
# ********************
from shared.utils import utils_logger

# ********************
# imports app
# ********************
from apps.subdashboard import models as subdashboard_models


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(
    operation_description="DELETE sub_dashboard interests of a user",
    methods=["DELETE"],
    responses={200: None},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request, email):

    if request.method == "DELETE":
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
                response_data.delete()

                return Response(None, status.HTTP_204_NO_CONTENT)
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
