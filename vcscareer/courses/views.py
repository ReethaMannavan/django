# vts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Course, UserCourseProgress

@login_required(login_url='login')
def pro_courses_view(request):
    courses = Course.objects.all()
    user_progress = {uc.course.id: uc.progress_percentage for uc in UserCourseProgress.objects.filter(user=request.user)}
    
    return render(request, 'courses/pro_courses.html', {
        'courses': courses,
        'user_progress': user_progress
    })
