from django.contrib import admin

# Register your models here.
# notes/admin.py

from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')  # Columns to show in admin list
    search_fields = ('title', 'content', 'owner__username')  # Searchable fields
    list_filter = ('owner',)  # Filter by owner

admin.site.register(Note, NoteAdmin)
