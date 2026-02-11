from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    total_modules = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


import uuid

class UserCourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_modules = models.PositiveIntegerField(default=0)

    # ✅ BRD additions
    enrolled_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)     # the “chosen course”
    is_completed = models.BooleanField(default=False)
    certificate_url = models.URLField(blank=True, null=True)


    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False)
    certificate_file = models.FileField(
        upload_to="certificates/",
        blank=True,
        null=True
    )

    @property
    def progress_percentage(self):
        if self.course.total_modules == 0:
            return 0
        return int((self.completed_modules / self.course.total_modules) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
