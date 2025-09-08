from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# List all tasks or create a new task
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        status_filter = self.request.query_params.get('status')
        if status_filter in ['Pending', 'Completed']:
            queryset = queryset.filter(status=status_filter)
        return queryset

# Retrieve, update, or delete a specific task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# FBV to mark a task as completed
@api_view(['PATCH'])
def mark_task_completed(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    task.status = 'Completed'
    task.save()
    serializer = TaskSerializer(task)
    return Response(serializer.data)
