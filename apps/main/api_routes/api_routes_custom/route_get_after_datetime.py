# ********************
# imports python
# ********************
from datetime import datetime

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
req_param_path_datetime = openapi.Parameter(
    "datetime",
    openapi.IN_QUERY,
    description="the datetime must be in UTC format e.g 2021-02-03 20:25:06",
    type=openapi.FORMAT_DATETIME,
)

# ******************************************
# CUSTOM RESPONSE SERIALIZER DEFINITION
# ******************************************


# respose http 200 definition
class Response200Serializer(serializers.Serializer):
    data = {}

    class Meta:
        ref_name = "apps.main_get_after_datetime_response200"


# respose http 400 definition
class Response400Serializer(serializers.Serializer):
    error = serializers.CharField()

    class Meta:
        ref_name = "apps.main_get_after_datetime_response400"


# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
@swagger_auto_schema(
    operation_description="GET action to get data created and updated after a datetime",
    methods=["GET"],
    manual_parameters=[req_param_path_datetime],
    responses={
        200: openapi.Response("response description", Response200Serializer),
        400: openapi.Response("response description", Response400Serializer),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):

    if request.method == "GET":
        req_param_datetime = request.GET.get("datetime", None)

        if req_param_datetime is None:
            # SERIALIZE AND RETURN
            return utils_drf.helper_json_response(
                Response400Serializer, {"error": "specify a datetime"}, status.HTTP_400_BAD_REQUEST
            )

        try:
            # get all created data after the datetime
            queryset_data_created = (
                main_models.Data.objects.filter(
                    created_at__gte=datetime.strptime(req_param_datetime, "%Y-%m-%d %H:%M:%S")
                )
                .select_related()
                .values()
            )

            # get all updated data after the datetime excluding
            # data in which created_at is not at least 10seconds less than updated_at
            # beacuse when a data-row is created the diffrence between the created_at and updated_at
            # fields are in miliseconds
            queryset_data_updated = (
                main_models.Data.objects.filter(
                    updated_at__gte=datetime.strptime(req_param_datetime, "%Y-%m-%d %H:%M:%S")
                )
                .select_related()
                .values()
            )

            filtered_data_created = []
            for data in queryset_data_created:
                filtered_data_created.append(
                    {
                        "id": data["id"],
                        "value": data["value"],
                        "period": data["period"],
                        "indicator": data["indicator_id"],
                        "datasource": data["datasource_id"],
                        "value_type": data["value_type_id"],
                        "location": data["location_id"],
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                    }
                )

            filtered_data_updated = []
            for data in queryset_data_updated:
                if ((data["updated_at"] - data["created_at"]).total_seconds()) > 10:
                    filtered_data_updated.append(
                        {
                            "id": data["id"],
                            "value": data["value"],
                            "period": data["period"],
                            "indicator": data["indicator_id"],
                            "datasource": data["datasource_id"],
                            "value_type": data["value_type_id"],
                            "location": data["location_id"],
                            "created_at": data["created_at"],
                            "updated_at": data["updated_at"],
                        }
                    )

        except Exception as e:
            # SERIALIZE AND RETURN
            return utils_drf.helper_json_response(
                Response400Serializer, {"error": str(e)}, status.HTTP_400_BAD_REQUEST
            )

        # SERIALIZE AND RETURN
        return utils_drf.helper_json_response(
            Response200Serializer,
            {"created": filtered_data_created, "updated": filtered_data_updated},
            status.HTTP_200_OK,
        )

    else:
        # SERIALIZE AND RETURN
        return utils_drf.helper_json_response(
            Response400Serializer, {"error": "bad request"}, status.HTTP_400_BAD_REQUEST
        )
