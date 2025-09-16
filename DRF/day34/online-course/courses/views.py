from rest_framework import viewsets
from .models import Course, Module, Lesson, Instructor
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer, InstructorSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('modules__lessons').all()
    serializer_class = CourseSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context  # this ensures 'request' is passed automatically


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.select_related('course').prefetch_related('lessons').all()
    serializer_class = ModuleSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('module', 'module__course').all()
    serializer_class = LessonSerializer

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.prefetch_related('courses').all()
    serializer_class = InstructorSerializer
