from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    """
    Custom permission: Patient can access their own appointments,
    staff/admin can access all appointments.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.patient == request.user
