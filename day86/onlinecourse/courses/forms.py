from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, InstructorProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=(('student', 'Student'), ('instructor', 'Instructor')))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['bio', 'avatar']

class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = ['bio', 'avatar']
