from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date', 'attendee_count')
    list_filter = ('date', 'organizer')
    search_fields = ('title', 'description', 'organizer__username')

    def attendee_count(self, obj):
        return obj.registrations.filter(status='REGISTERED').count()
    attendee_count.short_description = 'Attendees'

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'registered_at')
    list_filter = ('status', 'registered_at')
    search_fields = ('event__title', 'user__username', 'user__email')
