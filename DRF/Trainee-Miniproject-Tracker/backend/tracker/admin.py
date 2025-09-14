from django.contrib import admin
from .models import MiniProject

@admin.register(MiniProject)
class MiniProjectAdmin(admin.ModelAdmin):
    list_display = ("title","assigned_to","assigned_by","status","priority","due_date","progress")
    list_filter = ("status","priority")
    search_fields = ("title","description")
