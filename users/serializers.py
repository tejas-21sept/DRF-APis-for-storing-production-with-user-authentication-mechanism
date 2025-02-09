import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "email",
            "role",
        ]

    def validate_username(self, value):
        if not re.match(r"^[a-zA-Z0-9_-]{5,30}$", value):
            raise serializers.ValidationError(
                "Username must contain only letters and numbers."
            )
        return value

    def validate_role(self, value):
        valid_roles = dict(CustomUser.ROLE_CHOICES).keys()
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid role selected.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
            password=validated_data["password"],
        )
        return user


class CustomTOkenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        data["role"] = self.user.role
        return data
