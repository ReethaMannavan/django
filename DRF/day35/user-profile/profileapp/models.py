# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # Extra field for v2
    phone = models.CharField(max_length=15, blank=True, null=True)
