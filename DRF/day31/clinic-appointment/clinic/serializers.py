from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, Appointment

# Nested User serializer for doctor info
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Doctor serializer
class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization']

# Appointment serializer
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'date', 'time', 'status']  # patient removed

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user  # auto-assign patient
        return super().create(validated_data)
