from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Event, Registration
from .forms import EventForm, EventSearchForm
from django.core.mail import send_mail
from django.conf import settings

# Permission mixin - only organizer can edit/delete
class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_authenticated and obj.organizer == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to modify this event.")
        return redirect('events:event_list')

# Event list with search, pagination & filter upcoming/past
class EventListView(ListView):
    model = Event
    paginate_by = 10
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        when = self.request.GET.get('when')
        now = timezone.now()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(organizer__username__icontains=q))
        if when == 'upcoming':
            qs = qs.filter(date__gte=now)
        elif when == 'past':
            qs = qs.filter(date__lt=now)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = EventSearchForm(self.request.GET or None)
        return ctx

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        event = self.get_object()
        ctx['is_registered'] = False
        ctx['registrations'] = event.registrations.select_related('user')
        if self.request.user.is_authenticated:
            ctx['is_registered'] = Registration.objects.filter(event=event, user=self.request.user, status=Registration.STATUS_REGISTERED).exists()
        return ctx

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Event created.")
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Event updated.")
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event_list')

# Register view (POST)
class RegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        # prevent organizers from registering to their own event (optional)
        if event.organizer == request.user:
            messages.warning(request, "Organizers are already associated with their events.")
            return redirect(event.get_absolute_url())

        reg, created = Registration.objects.get_or_create(event=event, user=request.user, defaults={'status': Registration.STATUS_REGISTERED})
        if created:
            messages.success(request, "Registered for event.")
            # send confirmation emails (non-fatal)
            try:
                send_mail(
                    subject=f"Registration confirmed: {event.title}",
                    message=f"Hi {request.user.username},\n\nYou registered for {event.title} on {event.date}.\n\n",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )
                # notify organizer
                send_mail(
                    subject=f"New registration: {event.title}",
                    message=f"{request.user.username} registered for your event {event.title}.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[event.organizer.email],
                    fail_silently=True,
                )
            except Exception:
                # never crash the view on email errors
                pass
        else:
            if reg.status == Registration.STATUS_CANCELLED:
                reg.status = Registration.STATUS_REGISTERED
                reg.save()
                messages.success(request, "Re-registered for event.")
            else:
                messages.info(request, "You are already registered.")
        return redirect(event.get_absolute_url())

# Unregister - POST
class UnregisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        reg = Registration.objects.filter(event=event, user=request.user, status=Registration.STATUS_REGISTERED).first()
        if not reg:
            messages.info(request, "You are not registered.")
            return redirect(event.get_absolute_url())
        reg.status = Registration.STATUS_CANCELLED
        reg.save()
        messages.success(request, "You have unregistered.")
        return redirect(event.get_absolute_url())





# events/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required for event notifications")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# events/views.py
# events/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login
            return redirect("events:event_list")
    else:
        form = CustomUserCreationForm()  # no errors displayed initially
    return render(request, "registration/signup.html", {"form": form})


from django.utils import timezone
from .models import Event

def upcoming_events(request):
    today = timezone.now().date()  # current date
    events = Event.objects.filter(date__gte=today).order_by('date')  # events today or in future
    return render(request, 'events/upcoming_events.html', {'events': events})

def past_events(request):
    today = timezone.now().date()
    events = Event.objects.filter(date__lt=today).order_by('-date')  # events before today
    return render(request, 'events/past_events.html', {'events': events})


from django.views.generic import ListView
from .models import Event

class UpcomingEventsView(ListView):
    model = Event
    template_name = 'events/upcoming_events.html'
    context_object_name = 'events'
    paginate_by = 2  # number of events per page
    ordering = ['date']  # soonest first
