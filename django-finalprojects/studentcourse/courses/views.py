from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView
from .models import Course, Enrollment, Assignment, StudentProfile
from .forms import EnrollmentForm, AssignmentForm, UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings

# Auth
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('course_list')  # redirect prevents message duplication
    else:
        form = UserRegisterForm()
    return render(request, 'courses/register.html', {'form': form})



def login_view(request):
    form = UserLoginForm(request.POST or None)  # Initialize form
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('course_list')  # replace with your homepage
        else:
            form.add_error(None, "Invalid username or password.")  # attach error to form

    return render(request, 'courses/login.html', {'form': form})



def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Logged out successfully.")
        return redirect('login')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Courses
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 5

    def get_queryset(self):
        qs = Course.objects.all()
        dept = self.request.GET.get('department')
        if dept:
            qs = qs.filter(department__icontains=dept)
        return qs

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

# Enrollment
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile = request.user.studentprofile
    enrollment, created = Enrollment.objects.get_or_create(student=profile, course=course)
    if created:
        messages.success(request, f"Enrolled in {course.title}")
    else:
        messages.info(request, f"Already enrolled in {course.title}")
    return redirect('course_detail', pk=course.id)

# Assignment
class AssignmentUploadView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'courses/assignment_form.html'

    def form_valid(self, form):
        form.instance.student = self.request.user.studentprofile
        response = super().form_valid(form)
        messages.success(self.request, "Assignment uploaded successfully.")
        return response

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


from django.shortcuts import render
from .models import Enrollment, Course

def home(request):
    user = request.user

    if user.is_authenticated:
        if user.is_staff:
            # Instructors see only courses they teach
            courses = Course.objects.filter(instructor=user)
        else:
            # Students see all courses (or filter enrolled later)
            courses = Course.objects.all()
    else:
        # Not logged in
        courses = []

    return render(request, "courses/home.html", {"courses": courses})



