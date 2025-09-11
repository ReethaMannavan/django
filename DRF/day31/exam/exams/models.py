from django.db import models
from django.contrib.auth.models import User

# Admin creates exams
class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Questions for each exam
class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[
            ('1', 'Option 1'),
            ('2', 'Option 2'),
            ('3', 'Option 3'),
            ('4', 'Option 4'),
        ]
    )

    def __str__(self):
        return f"{self.exam.title} - {self.question_text[:50]}"

# Track which student took which exam
class StudentExam(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"
