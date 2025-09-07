from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    image = models.ImageField(
        upload_to='events/posters/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Registration',
        related_name='events_attending',
        blank=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} @ {self.organizer}"

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.pk])

    def is_upcoming(self):
        return self.date >= timezone.now()

class Registration(models.Model):
    STATUS_REGISTERED = 'REGISTERED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_REGISTERED, 'Registered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_REGISTERED)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user} -> {self.event.title} ({self.status})"


from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields you need
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
