from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),  

      # Pro user features
    path('pro/resume-optimize/', views.pro_resume_optimize, name='pro-resume-optimize'),
    path('pro/job-matching/', views.pro_job_matching, name='pro-job-matching'),
    path('pro/courses/', views.pro_courses, name='pro-courses'),
    path('pro/consultant/', views.pro_consultant, name='pro-consultant'),

    path('pro/feature/', views.pro_feature_placeholder, name='pro-feature'),
 


]
