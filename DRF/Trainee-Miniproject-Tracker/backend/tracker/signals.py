from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = "Welcome to Trainee Mini Project Tracker"
        message = (
            f"Hello {instance.username},\n\n"
            "Welcome to the Trainee Mini Project Tracker. You can now log in and start using the platform.\n\n"
            "Regards,\nTeam"
        )
        try:
            # from_email None uses DEFAULT_FROM_EMAIL in settings
            send_mail(subject, message, None, [instance.email])
        except Exception as e:
            # In dev avoid failing user creation — log to console
            print("Failed to send welcome email:", e)
