from django.db import models

# Create your models here.
# notes/models.py

from django.contrib.auth.models import User
from django.urls import reverse

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note-detail', kwargs={'pk': self.pk})
