from rest_framework.permissions import BasePermission, IsAuthenticated

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class IsSignUp(IsAuthenticated):
    def has_permission(self, request, view):
        return 'user_otp' in request.session or request.user.is_authenticated


class CanViewListing(BasePermission):
    def has_permission(self, request, view):
        return request.user.phone_number_verified