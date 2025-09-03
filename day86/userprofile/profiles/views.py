from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserRegistrationForm

# Existing profile detail
@login_required
def profile_detail(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_detail.html', {'form': form, 'profile': profile})

# New: Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            login(request, user)  # log in the new user immediately
            return redirect('profile_detail')
    else:
        form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'form': form})
