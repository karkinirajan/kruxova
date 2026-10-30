# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# *****************************************
# IMPORTs app
# *****************************************
from apps.main import models as main_models

from apps.dmi.api_routes.api_routes_crud import api_routes_crud_serializers


class DataViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = main_models.Data.objects.all()
    serializer_class = api_routes_crud_serializers.DataSerializer
