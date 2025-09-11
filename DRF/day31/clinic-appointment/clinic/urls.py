from django.urls import path
from .views import (
    DoctorListView,
    BookAppointmentView,
    PatientAppointmentsView,
    DoctorAppointmentsView,
    UpdateAppointmentStatusView
)

urlpatterns = [
    # Patient
    path("appointments/book/", BookAppointmentView.as_view(), name="book-appointment"),
    path("appointments/my/", PatientAppointmentsView.as_view(), name="my-appointments"),

    # Doctor
    path("appointments/doctor/", DoctorAppointmentsView.as_view(), name="doctor-appointments"),

    # Staff/Admin
    path("appointments/update/<int:id>/", UpdateAppointmentStatusView.as_view(), name="update-appointment"),

    # General
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
]
