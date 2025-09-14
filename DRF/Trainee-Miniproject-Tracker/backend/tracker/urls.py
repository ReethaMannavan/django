from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiniProjectViewSet, RegisterView, profile, public_mini_projects, trainees_list
from .views import mini_project_report

router = DefaultRouter()
router.register("mini-projects", MiniProjectViewSet, basename="mini-projects")  # Single route

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/profile/", profile, name="profile"),
    path("public-mini-projects/", public_mini_projects),  # Public endpoint for HomePage
    path("auth/trainees/", trainees_list, name="trainees-list"),
    path("reports/mini-projects/", mini_project_report, name="mini-project-report"),
]
