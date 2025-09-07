from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Registration
from django.core.mail import send_mail
from django.conf import settings

# Auto-create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Ensure profile is saved whenever user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Notify on Registration creation
@receiver(post_save, sender=Registration)
def notify_on_registration(sender, instance, created, **kwargs):
    if created and instance.status == Registration.STATUS_REGISTERED:
        try:
            send_mail(
                subject=f"Registration confirmed: {instance.event.title}",
                message=f"Hi {instance.user.username}, you registered for {instance.event.title}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=True,
            )
            send_mail(
                subject=f"New registration: {instance.event.title}",
                message=f"{instance.user.username} registered for your event.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.event.organizer.email],
                fail_silently=True,
            )
        except Exception:
            pass
