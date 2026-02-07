from django.urls import path
from .views import request_consultant,my_consultant_requests,admin_consultant_requests

urlpatterns = [
    path('request/', request_consultant, name='consultant-request'),
  
    path('my-requests/', my_consultant_requests, name='my-consultant-requests'),
    path('admin/requests/', admin_consultant_requests, name='admin-consultant-requests'),

]
