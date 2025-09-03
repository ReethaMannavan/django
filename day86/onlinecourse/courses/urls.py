from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/register/')),  # redirect root to /register/
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),

]
