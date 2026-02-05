from django.urls import path
from . import views

urlpatterns = [
    path('pro-courses/', views.pro_courses_view, name='pro-courses'),
]
