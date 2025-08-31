from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Student, Course, Enrollment
from .forms import StudentForm, CourseForm, StudentSearchForm

# List all students (CBV)
class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(name__icontains=query) | queryset.filter(email__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = StudentSearchForm(self.request.GET or None)
        return context

# Student detail with enrolled courses
class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"

# Add new student
@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("students:student_list")
    else:
        form = StudentForm()
    return render(request, "students/student_form.html", {"form": form})

# Staff-only course management
@user_passes_test(lambda u: u.is_staff)
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("students:course_list")
    else:
        form = CourseForm()
    return render(request, "students/course_form.html", {"form": form})

def course_list(request):
    courses = Course.objects.all()
    return render(request, "students/course_list.html", {"courses": courses})

# Enroll student in a course
@login_required
def enroll_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    courses = Course.objects.all()
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        Enrollment.objects.create(student=student, course=course)
        return redirect("students:student_detail", pk=student.id)
    return render(request, "students/enroll.html", {"student": student, "courses": courses})
