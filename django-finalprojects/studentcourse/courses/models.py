from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def assignment_upload_path(instance, filename):
    return f'assignments/course_{instance.course.id}/student_{instance.student.user.id}/{filename}'

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})
    description = models.TextField()
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.roll_number})"

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(default=timezone.now)
    grade = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} -> {self.course}"

class Assignment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to=assignment_upload_path)
    submitted_at = models.DateTimeField(default=timezone.now)
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.course.title} - {self.student.user.username}"
