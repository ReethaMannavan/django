from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MiniProject

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]



from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[("trainee","trainee"),("trainer","trainer")], write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", "trainee")
        user = User.objects.create_user(**validated_data)
        if role == "trainer":
            user.is_staff = True
            user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role"] = "trainer" if instance.is_staff else "trainee"
        return data



class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]

    def get_role(self, obj):
        return "trainer" if obj.is_staff else "trainee"


class MiniProjectSerializer(serializers.ModelSerializer):
    assigned_to = UserSummarySerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="assigned_to", write_only=True, required=False, allow_null=True
    )
    assigned_by = UserSummarySerializer(read_only=True)

    class Meta:
        model = MiniProject
        fields = [
            "id","title","description","assigned_to","assigned_to_id","assigned_by",
            "priority","status","progress","due_date","created_at","updated_at"
        ]
        read_only_fields = ["assigned_by","created_at","updated_at"]

    def validate_progress(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Progress must be between 0 and 100")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["assigned_by"] = request.user
        return super().create(validated_data)

class MiniProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniProject
        fields = ["title","description","priority","status","progress","due_date"]



