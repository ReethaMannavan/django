from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_detail, name='profile_detail'),
    path('register/', views.register, name='register'),
]
