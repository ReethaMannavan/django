from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    signup_view, logout_view,
    JobListView, JobDetailView, JobCreateView,
    EmployerDashboardView, JobUpdateView, JobDeleteView, ApplicationCreateView
)
from .forms import StyledAuthenticationForm

app_name = 'jobapp'

urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('signup/', signup_view, name='signup'),
    path('login/', LoginView.as_view(
    template_name='registration/login.html',
    authentication_form=StyledAuthenticationForm
), name='login'),

    path('logout/', logout_view, name='logout'),

    path('post/', JobCreateView.as_view(), name='job_post'),
    path('dashboard/', EmployerDashboardView.as_view(), name='employer_dashboard'),

    path('<int:job_pk>/apply/', ApplicationCreateView.as_view(), name='job_apply'),

    path('<int:pk>/edit/', JobUpdateView.as_view(), name='job_edit'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
]
