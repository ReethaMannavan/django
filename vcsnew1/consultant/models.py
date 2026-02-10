from django.db import models
from django.conf import settings

class ConsultantRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultant_requests'
    )
    purpose = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.purpose}"


#mockinterview
from django.conf import settings
from django.db import models


class MockInterview(models.Model):
    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    INTERVIEW_TYPES = (
        ("behavioral", "Behavioral"),
        ("technical", "Technical"),
        ("case_study", "Case Study"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES)
    target_role = models.CharField(max_length=150)
    scheduled_at = models.DateTimeField()

    meeting_link = models.URLField(blank=True, null=True)
    feedback = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Mock Interview"

