from django.urls import path
from .views import (
    BlogPostListCreateView,
    BlogPostDetailView,
    comments_for_post,
    add_comment
)

urlpatterns = [
    # BlogPost CRUD
    path('posts/', BlogPostListCreateView.as_view(), name='blogpost-list-create'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost-detail'),

    # Comments
    path('posts/<int:post_id>/comments/', comments_for_post, name='comments-for-post'),
    path('posts/<int:post_id>/comments/add/', add_comment, name='add-comment'),
]
