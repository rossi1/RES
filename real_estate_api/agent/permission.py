from rest_framework.permissions import BasePermission

class IsAgent(BasePermission):
    def has_object_permission(self, request, view):
        return request.user.is_agent