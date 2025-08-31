from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# TaskForm
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_completed']

# Filter by date (manual form)
class TaskFilterForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)

# Custom User registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
