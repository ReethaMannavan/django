from django.urls import path
from .views import (
    home, CourseDetailView, enroll_course, AssignmentUploadView,
    register_view, login_view, logout_view
)

urlpatterns = [
    path('', home, name='course_list'),  # homepage shows courses
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('assignment/upload/', AssignmentUploadView.as_view(), name='assignment_upload'),

    # Auth
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
