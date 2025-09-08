from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BlogSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Search blogs...'
    }))
    category = forms.ModelChoiceField(queryset=None, required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'})
        }

# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

