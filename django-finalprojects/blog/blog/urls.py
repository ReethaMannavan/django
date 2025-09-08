from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog post CRUD
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comment CRUD (all via Post detail page)
    path('post/<int:post_pk>/comment/add/', views.CommentCreateView.as_view(), name='comment_add'),

    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
