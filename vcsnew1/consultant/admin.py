from django.contrib import admin
from .models import ConsultantRequest

@admin.register(ConsultantRequest)
class ConsultantRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'purpose', 'status', 'created_at')
    list_filter = ('status',)
