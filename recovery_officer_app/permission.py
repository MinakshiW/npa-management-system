from rest_framework.permissions import BasePermission

class IsRecoveryOfficer(BasePermission):
    message = 'Only recovery officers are allowed to access this resource...'

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        return hasattr(request.user, 'recovery_officer')