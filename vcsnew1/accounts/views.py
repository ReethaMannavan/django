from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()  # CustomUser

# -------------------- Registration --------------------


def register_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

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

        if errors:
            context['errors'] = errors
            context['username'] = username
            context['email'] = email
        else:
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                subscription_tier='free'
            )
            user.save()

            user = authenticate(request, username=username, password=password)
            login(request, user)

            request.session['registration_success'] = True
            return redirect('home')

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




from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def dashboard_view(request):
    user = request.user

    # Admin Dashboard
    if user.is_staff or user.is_superuser:
        return render(request, 'accounts/admin_dashboard.html', {'user': user})

    # Candidate Dashboard (Free / Pro / Pro Plus)
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
    if user.subscription_tier not in ['free', 'pro', 'pro_plus']:

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
    if request.user.subscription_tier not in ['pro', 'pro_plus']:

        messages.error(request, "Upgrade to Pro to access this feature.")
        return redirect('dashboard')

    return render(request, 'accounts/pro_placeholder.html')





from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from jobs.models import Job, JobApplication, SavedJob

User = get_user_model()

def admin_analytics(request):
    # Only admin users allowed
    if not request.user.is_authenticated or (not request.user.is_superuser and request.user.role != 'admin'):
        return redirect('dashboard')

    total_users = User.objects.count()
    free_users = User.objects.filter(subscription_tier='free').count()
    pro_users = User.objects.filter(subscription_tier='pro').count()
    pro_plus_users = User.objects.filter(subscription_tier='pro_plus').count()

    conversion_rate = round((pro_users / total_users * 100), 1) if total_users else 0

    total_jobs = Job.objects.count()
    total_applications = JobApplication.objects.count()
    total_saved_jobs = SavedJob.objects.count()

    context = {
        'total_users': total_users,
        'free_users': free_users,
        'pro_users': pro_users,
        'conversion_rate': conversion_rate,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_saved_jobs': total_saved_jobs,
    }
    return render(request, 'accounts/admin_analytics.html', context)




#Revised
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta

@login_required
def upgrade_to_pro(request):
    user = request.user

    user.subscription_tier = "pro"
    user.subscription_expiry = timezone.now().date() + timedelta(days=30)
    user.pending_downgrade = None
    user.save()

    messages.success(request, "Upgraded to Pro plan.")
    return redirect("dashboard")



@login_required
def upgrade_to_proplus(request):
    user = request.user

    user.subscription_tier = "pro_plus"
    user.subscription_expiry = timezone.now().date() + timedelta(days=365)
    user.pending_downgrade = None
    user.save()

    messages.success(request, "Upgraded to Pro Plus plan.")
    return redirect("dashboard")




#downgrade
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def downgrade_free(request):
    request.user.pending_downgrade = "free"
    request.user.save()

    messages.success(request, "Your plan will downgrade at the end of billing cycle.")
    return redirect("subscription")


@login_required
def downgrade_pro(request):
    request.user.pending_downgrade = "pro"
    request.user.save()

    messages.success(request, "Your plan will downgrade at the end of billing cycle.")
    return redirect("subscription")








#subscription
from django.contrib.auth.decorators import login_required

@login_required
def subscription_view(request):
    return render(request, "accounts/subscription.html")




