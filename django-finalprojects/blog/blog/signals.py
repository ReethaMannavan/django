from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Post
from django.core.mail import send_mail
from django.conf import settings

# Auto-create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # uncommented, now active

# Ensure profile is saved whenever user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Notify all users (except author) when a new Post is created
@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subscribers = User.objects.exclude(pk=instance.author.pk).exclude(email__isnull=True).exclude(email__exact='')
        for user in subscribers:
            try:
                send_mail(
                    subject=f"New Blog Posted: {instance.title}",
                    message=f"Hi {user.username},\n\nA new blog was posted by {instance.author.username}.\n\n"
                            f"Read it here: {settings.SITE_URL}{instance.get_absolute_url()}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
            except Exception:
                pass
