
from django.urls import path
from .views import (
    JobListView, JobDetailView, ApplyJobView,
    save_job, unsave_job, SavedJobsView
)
from .views import (
    AdminJobListView,
    AdminJobCreateView,
    AdminJobUpdateView,
    AdminJobDeleteView,
    AdminApplicationListView
)

from .views import ProJobMatchingView

from .views import pro_interview_chatbot, pro_interview_chatbot_api
urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/apply/', ApplyJobView.as_view(), name='job-apply'),

    path('<int:pk>/save/', save_job, name='save-job'),
    path('<int:pk>/unsave/', unsave_job, name='unsave-job'),
    path('saved/', SavedJobsView.as_view(), name='saved-jobs'),

    path('admin/jobs/', AdminJobListView.as_view(), name='admin-job-list'),
    path('admin/jobs/create/', AdminJobCreateView.as_view(), name='admin-job-create'),
    path('admin/jobs/<int:pk>/update/', AdminJobUpdateView.as_view(), name='admin-job-update'),
    path('admin/jobs/<int:pk>/delete/', AdminJobDeleteView.as_view(), name='admin-job-delete'),
    # Admin Applications
   path('admin/applications/', AdminApplicationListView.as_view(), name='admin-applications'),

   #prouser
   # jobs/urls.py
path(
    'pro/job-matching/',
    ProJobMatchingView.as_view(),
    name='pro-job-matching'
),


    path('pro/interview-chatbot/', pro_interview_chatbot, name='pro-interview-chatbot'),
    path('pro/interview-chatbot/api/', pro_interview_chatbot_api, name='pro-interview-chatbot-api'),




]
