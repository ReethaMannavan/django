from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.StudentListView.as_view(), name="student_list"),
    path("student/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("student/add/", views.add_student, name="add_student"),
    path("course/add/", views.add_course, name="add_course"),
    path("courses/", views.course_list, name="course_list"),
    path("student/<int:student_id>/enroll/", views.enroll_student, name="enroll_student"),
]
