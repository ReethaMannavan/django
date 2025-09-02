from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeaveListView.as_view(), name='leave-list'),
    path('leave/new/', views.LeaveCreateView.as_view(), name='leave-create'),
    path('leave/<int:pk>/update/', views.LeaveUpdateView.as_view(), name='leave-update'),
    path('leave/<int:pk>/delete/', views.LeaveDeleteView.as_view(), name='leave-delete'),
    path('leave/<int:pk>/approve/', views.approve_leave, name='leave-approve'),
    path('leave/<int:pk>/reject/', views.reject_leave, name='leave-reject'),
]
