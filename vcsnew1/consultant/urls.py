from django.urls import path
from .views import request_consultant,my_consultant_requests,admin_consultant_requests

from .views import schedule_mock_interview
from .views import admin_mock_interviews, my_mock_interviews

urlpatterns = [
    path('request/', request_consultant, name='consultant-request'),
  
    path('my-requests/', my_consultant_requests, name='my-consultant-requests'),
    path('admin/requests/', admin_consultant_requests, name='admin-consultant-requests'),

    #mockinterview
    path("mock-interview/", schedule_mock_interview, name="schedule-mock"),
    path("admin/mock-interviews/", admin_mock_interviews, name="admin-mock-interviews"),
    path("my-mock-interviews/", my_mock_interviews, name="my-mock-interviews"),

]
