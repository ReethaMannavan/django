from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    TIER_CHOICES = (
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('pro_plus', 'Pro Plus'),
    )

    subscription_tier = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        default='free'
    )

    # NEW — subscription lifecycle fields
    subscription_expiry = models.DateField(null=True, blank=True)
    pending_downgrade = models.CharField(
        max_length=10,
        choices=TIER_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.subscription_tier})"




#candidateprofile
# accounts/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_resume_file(value):
    # Allowed extensions
    valid_extensions = ['pdf', 'doc', 'docx']
    ext = value.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Only PDF, DOC, DOCX files are allowed.')

    # Max size = 5MB
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Max size is 5MB.')

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    experience = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)  # in years
    skills = models.TextField(blank=True, null=True)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True,
        validators=[validate_resume_file]
    )

    def __str__(self):
        return self.user.username

    def profile_completion(self):
        """Return percentage of profile completeness"""
        fields = [self.full_name, self.phone, self.experience, self.skills, self.resume]
        filled = sum([1 for f in fields if f])
        return int((filled / len(fields)) * 100)




