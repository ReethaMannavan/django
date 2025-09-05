# reviews/admin.py
from django.contrib import admin
from .models import Book, Review, Category

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ("user", "rating", "comment", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("author", "categories")
    search_fields = ("title", "author")
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating", "book__author")
    search_fields = ("book__title", "user__username", "comment")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
