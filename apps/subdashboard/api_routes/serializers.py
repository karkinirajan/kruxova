# ********************
# imports python
# ********************
# ********************
# imports django
# ********************
from apps.subdashboard import models
from rest_framework import serializers


class CustomRoutesDefaultSerializerInterest(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    email = serializers.CharField(max_length=255, read_only=False, required=True)

    dashboard = serializers.CharField(max_length=255, read_only=False, required=True)

    created = serializers.CharField(max_length=100, read_only=False, required=False)

    created_at = serializers.DateTimeField(read_only=True, required=False)

    updated_at = serializers.DateTimeField(read_only=True, required=False)

    def create(self, validated_data):
        """
        Create and return a new `Interest` instance, given the validated data.
        """

        return models.Interest.objects.create(**validated_data)
