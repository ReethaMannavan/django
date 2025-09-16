from rest_framework import serializers
from .models import Course, Module, Lesson, Instructor

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content']

class ModuleSerializer(serializers.ModelSerializer):
    # HyperlinkedRelatedField for lessons
    lessons = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='lesson-detail'
    )

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'lessons']

class CourseSerializer(serializers.ModelSerializer):
    modules = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='module-detail'
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'modules']

class InstructorSerializer(serializers.ModelSerializer):
    courses = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='course-detail'
    )

    class Meta:
        model = Instructor
        fields = ['id', 'user', 'courses']
