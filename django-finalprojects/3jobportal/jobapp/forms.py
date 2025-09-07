from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Job, Application

# Signup
class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username','email','role','password1','password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

# Login
class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

# Job form
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','company','location','description']

# Job search
class JobSearchForm(forms.Form):
    q = forms.CharField(required=False,label='Keyword')
    location = forms.CharField(required=False,label='Location')

# Application form
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume','cover_letter']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['resume'].widget.attrs.update({'accept':'.pdf,.doc,.docx'})

    def clean_resume(self):
        f = self.cleaned_data.get('resume')
        max_mb = 5
        if f.size > max_mb*1024*1024:
            raise forms.ValidationError("File too large (max 5MB)")
        return f
