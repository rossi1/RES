from rest_framework.permissions import BasePermission

class IsServices(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_developer or 
    request.user.is_government or request.user.is_valuer)