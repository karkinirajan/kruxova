# ********************
# imports python
# ********************
import random

# ********************
# imports django
# ********************
from apps.user import models
from django.contrib.auth import get_user_model
from rest_framework import serializers


class CustomRoutesDefaultSerializerUser(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    user_id = serializers.CharField(max_length=255, read_only=False, required=False)

    name = serializers.CharField(max_length=255, read_only=False, required=True)

    username = serializers.CharField(max_length=255, read_only=False, required=True)

    profession = serializers.CharField(max_length=255, read_only=False, required=True)

    organization = serializers.CharField(max_length=255, read_only=False, required=True)

    email = serializers.CharField(max_length=255, read_only=False, required=True)

    email_verified_at = serializers.DateTimeField(read_only=True, required=False)

    # exclude password form data sent
    password = serializers.CharField(max_length=255, write_only=True, required=False)

    remember_token = serializers.CharField(max_length=100, read_only=False, required=False)

    created_at = serializers.DateTimeField(read_only=True, required=False)

    updated_at = serializers.DateTimeField(read_only=True, required=False)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        # generate random 20-char interger-strings
        validated_data["user_id"] = str(random.randint(00000000000000000000, 99999999999999999999))

        return models.User.objects.create(**validated_data)


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
