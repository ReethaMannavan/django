# serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

# Registration serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# v1 serializer: basic profile
class ProfileSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# v2 serializer: advanced profile
class ProfileSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'phone')
