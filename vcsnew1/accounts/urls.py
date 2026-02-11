from django.urls import path
from . import views
from .views import admin_analytics
from .views import billing_history, download_invoice


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),  

      # Pro user features
    path('pro/resume-optimize/', views.pro_resume_optimize, name='pro-resume-optimize'),
    path('pro/job-matching/', views.pro_job_matching, name='pro-job-matching'),
    path('pro/consultant/', views.pro_consultant, name='pro-consultant'),

    path('pro/feature/', views.pro_feature_placeholder, name='pro-feature'),

    path('admin/analytics/', admin_analytics, name='admin-analytics'),


#revised
path('upgrade/pro/', views.upgrade_to_pro, name='upgrade-pro'),
path('upgrade/proplus/', views.upgrade_to_proplus, name='upgrade-proplus'),

#downgrade
path('downgrade/free/', views.downgrade_free, name='downgrade-free'),
path('downgrade/pro/', views.downgrade_pro, name='downgrade-pro'),

#subscription
path('subscription/', views.subscription_view, name='subscription'),

#resumeoptimization
path("resume-optimizer/", views.resume_optimizer, name="resume-optimizer"),
path(
    "download-resume-pdf/",
    views.download_optimized_resume_pdf,
    name="download-optimized-resume-pdf",
),


#billing
path("billing/", billing_history, name="billing-history"),

path("invoice/<int:invoice_id>/download/", download_invoice, name="download-invoice"),


]
