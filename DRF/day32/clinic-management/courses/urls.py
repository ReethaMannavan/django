from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityViewSet, DepartmentViewSet, CourseViewSet

router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
