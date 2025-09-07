from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, EmployerProfile, ApplicantProfile

@receiver(post_save, sender=CustomUser)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.ROLE_EMPLOYER:
            EmployerProfile.objects.create(user=instance)
        elif instance.role == CustomUser.ROLE_APPLICANT:
            ApplicantProfile.objects.create(user=instance)
