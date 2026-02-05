from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()  # CustomUser

# -------------------- Registration --------------------
def register_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'free')

        # Field errors
        errors = {}
        if not username:
            errors['username'] = "Username is required"
        elif User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists"

        if not email:
            errors['email'] = "Email is required"
        elif User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists"

        if not password:
            errors['password'] = "Password is required"

        if role not in ['free', 'pro']:
            errors['role'] = "Select a valid role"

        if errors:
            context['errors'] = errors
            context['username'] = username
            context['email'] = email
            context['role'] = role
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )
            user.save()
            return redirect('login')

    return render(request, 'accounts/register.html', context)


# -------------------- Login --------------------
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            context['error'] = "Username and password are required"
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # Redirect ALL users to unified dashboard
                return redirect('dashboard')
            else:
                context['error'] = "Invalid username or password"

    return render(request, 'accounts/login.html', context)


# -------------------- Logout --------------------
def logout_view(request):
    logout(request)
    return redirect('login')


#rolebased
# from django.contrib.auth.decorators import login_required

# @login_required(login_url='login')
# def dashboard_view(request):
#     user = request.user

#     # ---------------- Admin Dashboard ----------------
#     if user.role == 'admin' or user.is_superuser:
#         return render(request, 'accounts/admin_dashboard.html')

#     # ---------------- Pro User Dashboard ----------------
#     if user.role == 'pro':
#         return render(request, 'accounts/dashboard_pro.html')

#     # ---------------- Free User Dashboard ----------------
#     return render(request, 'accounts/dashboard.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def dashboard_view(request):
    user = request.user

    # ---------------- Admin Dashboard ----------------
    if user.role == 'admin' or user.is_superuser:
        return render(request, 'accounts/admin_dashboard.html', {'user': user})

    # ---------------- Free & Pro User Dashboard ----------------
    return render(request, 'accounts/dashboard.html', {'user': user})




#candidateprofile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CandidateProfile
from .forms import CandidateProfileForm

@login_required
def profile_view(request):
    user = request.user

    # Only Free/Pro users can access
    if user.role not in ['free', 'pro']:
        messages.error(request, "Your account cannot access this page.")
        return redirect('dashboard')

    profile, created = CandidateProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully saved!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateProfileForm(instance=profile)

    completion = profile.profile_completion()

    return render(request, 'accounts/profile.html', {
        'form': form,
        'completion': completion
    })


#prouser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def pro_resume_optimize(request):
    user = request.user
    return render(request, 'accounts/pro_resume_optimize.html', {'user': user})

@login_required(login_url='login')
def pro_job_matching(request):
    user = request.user
    # TODO: add skills-based matching logic
    matched_jobs = []  # placeholder
    return render(request, 'accounts/pro_job_matching.html', {'user': user, 'matched_jobs': matched_jobs})

@login_required(login_url='login')
def pro_courses(request):
    user = request.user
    return render(request, 'accounts/pro_courses.html', {'user': user})

@login_required(login_url='login')
def pro_consultant(request):
    user = request.user
    return render(request, 'accounts/pro_consultant.html', {'user': user})



#placeholder pro
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def pro_feature_placeholder(request):
    if request.user.role != 'pro':
        messages.error(request, "Upgrade to Pro to access this feature.")
        return redirect('dashboard')

    return render(request, 'accounts/pro_placeholder.html')
