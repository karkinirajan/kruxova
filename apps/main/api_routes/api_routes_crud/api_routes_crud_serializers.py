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
from django.contrib.auth import get_user_model

# ********************************************************************************
# APP_MAIN MODELS CRUD(DEFAULT) SERIALIZERS
# ********************************************************************************


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Group
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Location
        fields = "__all__"


class LocationHierarchyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.LocationHierarchyLevel
        fields = "__all__"


class ValueTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    value_type = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = main_models.ValueType


class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Factor
        fields = "__all__"


class DatasourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Datasource
        fields = "__all__"


class DatasourceValuetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.DatasourceValuetype
        fields = "__all__"


class DatasourceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.DatasourceLocation
        fields = "__all__"


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Indicator
        fields = "__all__"


class IndicatorValuetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.IndicatorValuetype
        fields = "__all__"


class DatasourceSpecificIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.DatasourceSpecificIndicator
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Link
        fields = "__all__"


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Data
        fields = "__all__"


class DisaggregatedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.DisaggregatedData
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Subscriber
        fields = "__all__"


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "username", "email", "password"]
        # the stored hash must never be serialised back to a client
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # create_user hashes the password; a plain ModelSerializer would store it as clear text
        return UserModel.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = main_models.Dashboard
        fields = "__all__"
