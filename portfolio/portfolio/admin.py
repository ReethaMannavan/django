from django.contrib import admin
from django.utils.html import format_html

from .models import Project, Skill, ContactMessage

# -------------------- Projects Admin --------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'link', 'image_tag')
    search_fields = ('title', 'description')
    list_filter = ('title',)
    readonly_fields = ('image_tag',)  # display image in admin
    ordering = ('title',)

    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    short_description.short_description = 'Description'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:5px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image Preview'

# -------------------- Skills Admin --------------------
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'proficiency_bar')
    search_fields = ('name',)
    list_editable = ('proficiency',)
    ordering = ('name',)

    def proficiency_bar(self, obj):
        return format_html(
            '<div style="background:#e0e0e0; border-radius:10px; width:100px;">'
            '<div style="background:#097AFA; width:{}%; height:10px; border-radius:10px;"></div>'
            '</div>', obj.proficiency)
    proficiency_bar.short_description = 'Proficiency'

# -------------------- Contact Messages Admin --------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'message', 'created_at')

    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'
