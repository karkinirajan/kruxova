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
from apps.user import models as user_models

from apps.user.api_routes.api_routes_crud import api_routes_crud_serializers


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = api_routes_crud_serializers.UserSerializer
    queryset = user_models.User.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = api_routes_crud_serializers.ContactSerializer
    queryset = user_models.Contact.objects.all()
