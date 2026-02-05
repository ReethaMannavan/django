# jobs/models.py or a new app vts/models.py
from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    total_modules = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.title


class UserCourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)
    
    @property
    def progress_percentage(self):
        if self.course.total_modules == 0:
            return 0
        return int((self.completed_modules / self.course.total_modules) * 100)
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
