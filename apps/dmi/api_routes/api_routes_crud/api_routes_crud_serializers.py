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
from apps.main import models as main_models


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Data
        fields = "__all__"
