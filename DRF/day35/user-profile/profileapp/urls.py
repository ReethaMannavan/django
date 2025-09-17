from django.urls import path
from .views import RegisterView, ProfileViewV1, ProfileViewV2

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('v1/profile/', ProfileViewV1.as_view(), name='profile-v1'),
    path('v2/profile/', ProfileViewV2.as_view(), name='profile-v2'),
]
