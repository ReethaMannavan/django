from django.urls import path
from .views import TaskListCreateView, TaskDetailView, mark_task_completed

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),  # no extra 'tasks/' here
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:task_id>/complete/', mark_task_completed, name='task-complete'),
]
