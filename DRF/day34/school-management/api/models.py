# api/models.py

from django.db import models

class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subjects = models.ManyToManyField(Subject, related_name='teachers')

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name
