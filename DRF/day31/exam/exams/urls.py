from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    AdminTestView,
    AdminCreateExamView,
    AdminAddQuestionView,
    ExamListView,
    SubmitExamView,
    HomeView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth / Student
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # JWT login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Admin
    path('admin-test/', AdminTestView.as_view(), name='admin-test'),
    path('admin-create-exam/', AdminCreateExamView.as_view(), name='admin-create-exam'),
    path('admin-add-question/<int:exam_id>/', AdminAddQuestionView.as_view(), name='admin-add-question'),

    # Student
    path('exams/', ExamListView.as_view(), name='exam-list'),
    path('submit-exam/<int:exam_id>/', SubmitExamView.as_view(), name='submit-exam'),

    path('', HomeView.as_view(), name='home'),
]
