from django import forms
from .models import CustomerQuery
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Contact form
class CustomerQueryForm(forms.ModelForm):
    class Meta:
        model = CustomerQuery
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'message': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 4}),
        }

# Registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }
