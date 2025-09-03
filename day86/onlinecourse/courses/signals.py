from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile, InstructorProfile
import os

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        role = getattr(instance, 'profile_role', 'student')
        if role == 'student':
            StudentProfile.objects.create(user=instance)
        else:
            InstructorProfile.objects.create(user=instance)

@receiver(post_delete, sender=StudentProfile)
def delete_student_avatar(sender, instance, **kwargs):
    if instance.avatar and os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)

@receiver(post_delete, sender=InstructorProfile)
def delete_instructor_avatar(sender, instance, **kwargs):
    if instance.avatar and os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)
