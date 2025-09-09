from rest_framework import serializers
from .models import Course, Instructor

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'name', 'email']


class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(),
        source='instructor',
        write_only=True
    )
    total_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_id', 'total_lessons']

    def get_total_lessons(self, obj):
        return obj.total_lessons

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Course title cannot be empty")
        return value
