from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, UserCourseProgress

@login_required(login_url="login")
def pro_courses_view(request):
    user = request.user

    # ✅ BRD tier enforcement
    if user.subscription_tier != "pro_plus":
        messages.error(request, "VTS Training is available only for Pro Plus users.")
        return redirect("subscription")

    courses = Course.objects.all()

    # user chosen course (active enrollment)
    active_enrollment = UserCourseProgress.objects.filter(
        user=user, is_active=True
    ).select_related("course").first()

    # progress mapping for UI
    user_progress = {
        uc.course.id: uc.progress_percentage
        for uc in UserCourseProgress.objects.filter(user=user)
    }

    return render(request, "courses/pro_courses.html", {
        "courses": courses,
        "user_progress": user_progress,
        "active_enrollment": active_enrollment,   # ✅ used for “1 course” rule display
    })


@login_required(login_url="login")
def select_course(request, course_id):
    user = request.user

    if user.subscription_tier != "pro_plus":
        messages.error(request, "VTS Training is available only for Pro Plus users.")
        return redirect("subscription")

    # already selected one course?
    if UserCourseProgress.objects.filter(user=user, is_active=True).exists():
        messages.error(request, "You already selected a course. Only 1 course is allowed for Pro Plus.")
        return redirect("pro-courses")

    course = get_object_or_404(Course, id=course_id)

    UserCourseProgress.objects.create(
        user=user,
        course=course,
        completed_modules=0,
        is_active=True
    )

    messages.success(request, f"You enrolled in: {course.title}")
    return redirect("pro-courses")




from .utils import generate_certificate

def complete_course(progress):
    progress.is_completed = True
    progress.save()

    if not progress.certificate_file:
        generate_certificate(progress)


from .utils import generate_certificate

@login_required
def complete_course_view(request, course_id):
    progress = get_object_or_404(
        UserCourseProgress,
        user=request.user,
        course_id=course_id
    )

    progress.completed_modules = progress.course.total_modules
    progress.is_completed = True
    progress.save()

    # Generate certificate file
    generate_certificate(progress)

    return redirect("pro-courses")

