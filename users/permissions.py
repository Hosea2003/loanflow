from rest_framework.permissions import BasePermission

from users.models import AppUser

class CanViewUser(BasePermission):
    def has_object_permission(self, request, view, obj:AppUser):
        user:AppUser = request.user
        if user.role==AppUser.AppUserRoles.CONSULTANT:
            return True
        return obj.id==user.id

class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        user:AppUser = request.user
        return user.role==AppUser.AppUserRoles.CONSULTANT