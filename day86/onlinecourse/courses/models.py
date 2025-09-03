from django.db import models
from django.contrib.auth.models import User
import os

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/students/', blank=True, null=True)
    # Optional: track enrolled courses
    # enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='students')

    def __str__(self):
        return f"{self.user.username}'s Student Profile"

class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/instructors/', blank=True, null=True)
    # Optional: track courses they create
    # courses = models.ManyToManyField('Course', blank=True, related_name='instructors')

    def __str__(self):
        return f"{self.user.username}'s Instructor Profile"

# Optional Course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
