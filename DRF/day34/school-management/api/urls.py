# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SchoolViewSet,
    StudentViewSet,
    TeacherViewSet,
    SubjectViewSet,
    StudentVariantViewSet,
    TeacherVariantViewSet
)

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'subjects', SubjectViewSet, basename='subject')

# the variant ones
router.register(r'students_variant', StudentVariantViewSet, basename='student-variant')
router.register(r'teachers_variant', TeacherVariantViewSet, basename='teacher-variant')

urlpatterns = [
    path('', include(router.urls)),
]
