from rest_framework.permissions import BasePermission


class IsValidUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_agent or request.user.is_property_owner


class CanPostListing(BasePermission):
    message = 'You cant upload any listing at the moment'

    def has_permission(self, request, view):
        return request.user.is_confirmed and request.user.phone_number_verified
