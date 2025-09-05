# reviews/urls.py (app)
from django.urls import path
from .views import (
    BookListView, BookDetailView,
    ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView,
    register_view, login_view, logout_view
)

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),

    path("books/<int:book_id>/reviews/add/", ReviewCreateView.as_view(), name="review_add"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review_detail"),
    path("reviews/<int:pk>/edit/", ReviewUpdateView.as_view(), name="review_edit"),
    path("reviews/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review_delete"),

    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
