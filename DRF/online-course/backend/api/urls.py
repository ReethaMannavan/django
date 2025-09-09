from django.urls import path
from .views import (
    CourseListCreateView,
    CourseRetrieveUpdateDeleteView,
    instructor_list_create,
    instructor_retrieve_update_delete
)

urlpatterns = [
    # Courses
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDeleteView.as_view(), name='course-detail'),

    # Instructors
    path('instructors/', instructor_list_create, name='instructor-list-create'),
    path('instructors/<int:pk>/', instructor_retrieve_update_delete, name='instructor-detail'),
]
