from django.urls import path
from .views import BlogView

urlpatterns = [
    path('v1/blogs/', BlogView.as_view(), name='blog-list-v1'),
    path('v1/blogs/<int:pk>/', BlogView.as_view(), name='blog-detail-v1'),
    path('v2/blogs/', BlogView.as_view(), name='blog-list-v2'),
    path('v2/blogs/<int:pk>/', BlogView.as_view(), name='blog-detail-v2'),
]
