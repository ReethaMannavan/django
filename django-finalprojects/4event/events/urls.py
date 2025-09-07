from django.urls import path
from . import views


app_name = "events"

urlpatterns = [
    path("", views.EventListView.as_view(), name="event_list"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    path("event/create/", views.EventCreateView.as_view(), name="event_create"),
    path("event/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_edit"),
    path("event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
    
    # Use CBVs here
    path("event/<int:pk>/register/", views.RegisterView.as_view(), name="event_register"),
    path("event/<int:pk>/unregister/", views.UnregisterView.as_view(), name="event_unregister"),
    

    # signup
    path("signup/", views.signup_view, name="signup"),
]
