from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, EmployerProfile, ApplicantProfile

@receiver(post_save, sender=CustomUser)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        # Create profile depending on role
        if instance.role == CustomUser.ROLE_EMPLOYER:
            EmployerProfile.objects.create(user=instance)
        elif instance.role == CustomUser.ROLE_APPLICANT:
            ApplicantProfile.objects.create(user=instance)

        # Send welcome email
        if instance.email:  # Only if email is provided
            subject = "Welcome to Job Portal"
            message = f"Hello {instance.username},\n\nThank you for registering as a {instance.role} on our Job Portal!"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
