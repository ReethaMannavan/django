from django import forms
from django.utils import timezone
from .models import Event, Registration
from django.conf import settings
from django.core.exceptions import ValidationError

class EventSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search events...'
    }))
    when = forms.ChoiceField(required=False, choices=[
        ('all', 'All'),
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))

class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Event
        fields = ['title', 'date', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_date(self):
        dt = self.cleaned_data['date']
        # Optionally disallow creating events with date far in the past:
        if dt < timezone.now() - timezone.timedelta(days=1):
            raise ValidationError("Event date can't be in the distant past.")
        return dt

    def clean_image(self):
        img = self.cleaned_data.get('image')
        if img:
            max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5 * 1024 * 1024)  # default 5MB
            if img.size > max_size:
                raise ValidationError(f"Image too large (max {max_size // (1024*1024)} MB).")
        return img

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []  # we create status/user server-side; no user input needed


# events/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter username'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter email'
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


