from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, StudentProfileForm, InstructorProfileForm


def home(request):
    return redirect('register')  # or render a template for homepage

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.profile_role = form.cleaned_data['role']
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'courses/register.html', {'form': form})

@login_required
def dashboard(request):
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile
        return render(request, 'courses/student_dashboard.html', {'profile': profile})
    elif hasattr(request.user, 'instructorprofile'):
        profile = request.user.instructorprofile
        return render(request, 'courses/instructor_dashboard.html', {'profile': profile})
    else:
        return redirect('logout')


from .forms import InstructorProfileForm

@login_required
def dashboard(request):
    if hasattr(request.user, 'instructorprofile'):
        profile = request.user.instructorprofile

        if request.method == 'POST':
            form = InstructorProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = InstructorProfileForm(instance=profile)

        return render(request, 'courses/instructor_dashboard.html', {
            'profile': profile,
            'form': form
        })
 




@login_required
def dashboard(request):
    # Student dashboard
    if hasattr(request.user, 'studentprofile'):
        profile = request.user.studentprofile

        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = StudentProfileForm(instance=profile)

        return render(request, 'courses/student_dashboard.html', {
            'profile': profile,
            'form': form
        })

    # Instructor dashboard
    elif hasattr(request.user, 'instructorprofile'):
        profile = request.user.instructorprofile

        if request.method == 'POST':
            form = InstructorProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = InstructorProfileForm(instance=profile)

        return render(request, 'courses/instructor_dashboard.html', {
            'profile': profile,
            'form': form
        })
    else:
        return redirect('logout')



