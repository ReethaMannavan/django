from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from .forms import ContactForm, UserRegisterForm

# Root redirect
def home(request):
    return redirect('add_contact')

# Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add_contact')
    else:
        form = UserRegisterForm()
    return render(request, 'contacts/register.html', {'form': form})

# Add contact form
@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()

            # Send email to admin
            send_mail(
                subject=f"New Contact from {contact.user.username}",
                message=f"Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}\nMessage: {contact.message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})

# Success page
def contact_success(request):
    return render(request, 'contacts/contact_success.html')


from django.contrib.auth.views import LoginView
from .forms import UserLoginForm

class CustomLoginView(LoginView):
    template_name = 'contacts/login.html'
    authentication_form = UserLoginForm
