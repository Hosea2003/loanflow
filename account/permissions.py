from rest_framework.permissions import BasePermission

from users.models import AppUser

class IsClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.role==AppUser.AppUserRoles.choices