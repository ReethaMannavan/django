from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} → {self.course.title}"
