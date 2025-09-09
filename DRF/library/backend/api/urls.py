from django.urls import path
from .views import (
    BookListCreateView, BookRetrieveUpdateDeleteView,
    author_list_create, author_update_delete
)

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookRetrieveUpdateDeleteView.as_view(), name="book-detail"),
    path("authors/", author_list_create, name="author-list-create"),
    path("authors/<int:pk>/", author_update_delete, name="author-update-delete"),
]
