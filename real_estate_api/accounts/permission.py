import jwt

from django.conf import settings


from rest_framework.permissions import BasePermission


from .validators import ValidityError


class ValidateSession(BasePermission):

    def has_permission(self, request, view):
        return 'otp_data' in request.session

class ValidateUser(BasePermission):

    def has_permission(self, request, view):
        return 'email' in request.session  or 'user_otp' in request.session or 'otp_code' in request.session

class ValidateResetPass(BasePermission):
    def has_permission(self, request, view):
        return 'email_data' in request.session or 'user' in request.session

class ValidateEmailReset(BasePermission):
    def has_permission(self, request, view):
        return 'code' in request.session


class ValidateResendOTP(BasePermission):
    def has_permission(self, request, view):
        return 'user_otp' in request.session or 'otp_code' in request.session or 'email' in request.session

class ValidateEmailCode(BasePermission):
    def has_permission(self, request, view):
        return 'email_code' in request.session

class ValidateEmailResendCode(BasePermission):
    def has_permission(self, request, view):
        return 'user' in request.session

class JwtAuthentication(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_TOKEN', None)

        if token is not None:
            try:
                token = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
            
            except jwt.ExpiredSignatureError:
                raise ValidityError({
                    'message': 'false',
                    'res': False,
                    'reason': 'Token expired'})
            
            except jwt.DecodeError:
                raise ValidityError({
                    'message': 'false',
                    'res': False,
                    'reason': 'Invalid Token'})

            else:
                if request.user.is_authenticated or token: 
                    return True
                else:
                    return False
                    
        if request.user.is_authenticated:
            return True
        return False

        
                