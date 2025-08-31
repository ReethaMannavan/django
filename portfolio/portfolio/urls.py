from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, contact_view,
    login_view, logout_view, project_create, register_view
)

app_name = "portfolio"

urlpatterns = [
    path("", ProjectListView.as_view(), name="index"),
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("contact/", contact_view, name="contact"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),  # <--- Add this line
    path("project/new/", project_create, name="project_create"),
]
