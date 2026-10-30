# ********************
# imports python
# ********************
import json
import logging

# **********************
# imports third-party
# **********************
from kombu.exceptions import OperationalError
from drf_yasg.utils import swagger_auto_schema

# ********************
# imports django
# ********************
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# ********************
# imports app
# ********************
from apps.data_caches import models as data_caches_models
from apps.data_caches import tasks

# ********************************
# CUSTOM SCHEMA DEFINITIONS
# ********************************
logger = logging.getLogger(__name__)


@swagger_auto_schema(
    operation_description="update all caches not currently in-progress", methods=["GET"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def route(request):
    if request.method == "GET":
        if can_refresh():
            try:
                tasks.task_update_data_caches.apply_async()
            except (OperationalError, OSError) as error:
                # the message broker (Redis) is unreachable: report it instead of a 500
                logger.error("cannot queue the cache refresh: %s", error)
                return HttpResponse(
                    json.dumps({"status": "BROKER_UNAVAILABLE"}),
                    content_type="application/json",
                    status=503,
                )

            response_data = {"status": "STARTED"}
        else:
            response_data = {"status": "ALREADY_INPROGRESS"}

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


def can_refresh():
    """
    check if a refresh can be made
    if any cache status is still in progress
    no refresh should start,all must end with fail or completed
    """
    caches = data_caches_models.DataCacheStatus.objects.all()

    if len(caches) == 0:
        # first time run
        return True
    else:
        for cache in caches:
            if cache.status == data_caches_models.CHOICES_STATUS_INPROGRESS:
                return False

        return True
