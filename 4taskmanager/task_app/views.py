from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Task
from .forms import TaskForm, TaskFilterForm, CustomUserCreationForm
from django.contrib.auth import login

# List tasks
class TaskListView(ListView):
    model = Task
    template_name = 'task_app/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Task.objects.filter(user=self.request.user)
            date = self.request.GET.get('date')
            if date:
                qs = qs.filter(due_date=date)
            return qs
        return Task.objects.none()

# Task detail
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_app/task_detail.html'
    context_object_name = 'task'

# Create task
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_app:task_list')
    else:
        form = TaskForm()
    return render(request, 'task_app/task_form.html', {'form': form})

# Edit task
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_app:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_app/task_form.html', {'form': form})

# Delete task
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_app:task_list')
    return render(request, 'task_app/task_confirm_delete.html', {'task': task})

# Custom registration
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome.")
            return redirect('task_app:task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'task_app/registration.html', {'form': form})
