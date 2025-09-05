from django.contrib import admin
from .models import Course, StudentProfile, Enrollment, Assignment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'department')
    search_fields = ('title', 'instructor__username')
    list_filter = ('department',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number')
    search_fields = ('roll_number', 'user__username')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled', 'grade')
    list_filter = ('course',)
    search_fields = ('student__roll_number', 'course__title')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'submitted_at', 'graded', 'grade')
    list_filter = ('graded', 'course')
