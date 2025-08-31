from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Course, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "email")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date")
