from rest_framework.permissions import BasePermission

class IsHotel(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_hotelier