from django import forms
from .models import Student, Course

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "age", "email"]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]

# Manual Form for Searching Students
class StudentSearchForm(forms.Form):
    query = forms.CharField(
        label="Search Student",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by name or email"})
    )
