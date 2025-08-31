from django import forms
from .models import Project, ContactMessage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "image", "link"]

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith(".com"):
            raise forms.ValidationError("Email must end with .com")
        return email
