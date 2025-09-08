from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

# Custom User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_EMPLOYER = 'employer'
    ROLE_APPLICANT = 'applicant'
    ROLE_CHOICES = [
        (ROLE_EMPLOYER, 'Employer'),
        (ROLE_APPLICANT, 'Applicant'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Fix clashes by adding related_name
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # changed from default 'user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # changed from default 'user_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    from django.urls import reverse

    def get_dashboard_url(self):
        if self.role == self.ROLE_EMPLOYER:
            return reverse('jobapp:employer_dashboard')
        else:
        # Redirect applicants to job list for now
            return reverse('jobapp:job_list')



# Employer Profile
class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"EmployerProfile({self.user.username})"

# Applicant Profile
class ApplicantProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='applicant_profile')
    headline = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"ApplicantProfile({self.user.username})"

# Job Model
class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company}"

    def get_absolute_url(self):
        return reverse('jobapp:job_detail', args=[self.pk])

# Application Model
STATUS_CHOICES = [('PENDING','Pending'),('REVIEWED','Reviewed'),('ACCEPTED','Accepted'),('REJECTED','Rejected')]

def resume_upload_to(instance, filename):
    return f"resumes/{instance.job.id}/{timezone.now().strftime('%Y%m%d_%H%M%S')}_{filename}"

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to=resume_upload_to, validators=[FileExtensionValidator(['pdf','doc','docx'])])
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job','applicant')

    def __str__(self):
        return f"{self.applicant} -> {self.job}"
