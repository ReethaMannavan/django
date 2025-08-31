from django.urls import path
from .views import (
    RecipeListView, RecipeDetailView,
    recipe_create, recipe_edit, recipe_delete
)
from . import views

app_name = "recipes"

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/new/', recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete/', recipe_delete, name='recipe_delete'),
]

