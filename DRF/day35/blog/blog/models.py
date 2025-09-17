from django.db import models
from django.contrib.auth.models import User

# v1 & v2 compatible Blog model
class Blog(models.Model):
    # models.py
    author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,  # allow null
    blank=True
)

    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # v2 fields
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)  # comma-separated
    view_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
