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
from shared.utils import utils_logger

# ********************
# imports app
# ********************
from apps.main import models as main_models

# *************************************************************************
# API ROUTE
# *************************************************************************


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(operation_description="GET count of all data", methods=["GET"])
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):
    if request.method == "GET":
        response_data = 0

        try:
            # ================================
            # RUN QUERIES
            # ================================

            data_count = main_models.Data.objects.count()

            # ================================
            # PACKAGE RESPONSE
            # ================================

            response_data = {"count": data_count}

            # LOG
            # utils_logger.log_print("RESPONSE DATA",response_data,param_oneline=False)

            # ================================
            # SERIALIZE RESPONSE
            # ================================
            data_serialized = json.dumps(response_data)
            return HttpResponse(data_serialized, content_type="application/json")

        except Exception as e:
            # LOG
            utils_logger.log_print("", str(e), param_oneline=True)

            # ================================
            # SERIALIZE RESPONSE
            # ================================
            data_serialized = json.dumps(response_data)
            return HttpResponse(data_serialized, content_type="application/json")
    else:
        # ================================
        # SERIALIZE RESPONSE
        # ================================
        data_serialized = json.dumps(response_data)
        return HttpResponse(data_serialized, content_type="application/json")
