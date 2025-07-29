from rest_framework import permissions


class IsConsultant(permissions.BasePermission):
    """
    Allows access only to users with consultant role.
    Assumes user model has a 'role' attribute.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'CONSULTANT'

class IsConsultantOrOwner(permissions.BasePermission):
    """
    Allows access to consultants or the owner of the loan.
    """
    def has_object_permission(self, request, view, obj):
        return (
            (hasattr(request.user, 'role') and request.user.role == 'CONSULTANT') or
            obj.user == request.user)