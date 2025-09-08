from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmployerProfile, ApplicantProfile, Job, Application

# CustomUser admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmployerProfile)
admin.site.register(ApplicantProfile)

# Job admin
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'created_by']

    def save_model(self, request, obj, form, change):
        # If created_by is not set, assign to the logged-in user if they are an employer
        if not obj.created_by_id:
            if hasattr(request.user, 'role') and request.user.role == 'employer':
                obj.created_by = request.user
            else:
                # fallback: pick any employer
                employer = CustomUser.objects.filter(role='employer').first()
                if employer:
                    obj.created_by = employer
                else:
                    raise ValueError("No employer exists to assign this job")
        super().save_model(request, obj, form, change)

admin.site.register(Job, JobAdmin)

# Application admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status',)
