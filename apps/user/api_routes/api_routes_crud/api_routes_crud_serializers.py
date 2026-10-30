# *****************************************
# IMPORTs python
# *****************************************

# *****************************************
# IMPORTs django
# *****************************************
from rest_framework import serializers

# *****************************************
# IMPORTs app
# *****************************************
from apps.user import models as user_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Contact
        fields = "__all__"
