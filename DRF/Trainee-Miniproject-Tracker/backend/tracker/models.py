from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  

class MiniProject(models.Model):
    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    STATUS_CHOICES = [
      
        ("assigned", "Assigned"),
        ("inprogress", "In Progress"),
        ("completed", "Completed"),
        
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="assigned_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="assigned")
    progress = models.PositiveSmallIntegerField(default=0)  # 0-100
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
