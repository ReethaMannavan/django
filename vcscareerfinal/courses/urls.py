from django.urls import path
from . import views

urlpatterns = [
    path("pro-courses/", views.pro_courses_view, name="pro-courses"),
    path("pro-courses/select/<int:course_id>/", views.select_course, name="select-course"),
    path("complete-course/<int:course_id>/", views.complete_course_view, name="complete-course"),

]

