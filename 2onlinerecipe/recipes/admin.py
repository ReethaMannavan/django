from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Recipe, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'ingredients', 'steps')
    list_filter = ('category', 'created_at')
