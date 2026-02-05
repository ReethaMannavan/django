from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


#candidateprofileform
from django import forms
from .models import CandidateProfile

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'phone', 'experience', 'skills', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1, 'min': 0}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'List your skills'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone must contain only digits.")
        return phone

    def clean_experience(self):
        exp = self.cleaned_data.get('experience')
        if exp is not None and exp < 0:
            raise forms.ValidationError("Experience cannot be negative.")
        return exp




