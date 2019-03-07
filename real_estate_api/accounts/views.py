import json
import re


from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.signing import TimestampSigner
from django.core.signing import BadSignature, SignatureExpired
from django.core.cache import cache

from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from .permission import (
    ValidateSession, ValidateUser,  
    ValidateResetPass, ValidateResendOTP, 
    ValidateEmailCode, ValidateEmailResendCode, JwtAuthentication
)
from .utils import Auth, account_type,account_image, account_full_name, encode_user_payload
from .serializer import (
    PropertyOwnerSerializer, AgentSerializer,
    DeveloperSerializer,
    HotelierSerializer, CustomerSerializer,
    GovernmentSerializer, PasswordResetNumberSerializer,
    LoginSerializer, OtpSerializer, PasswordResetSerializer,
    SupplierSerializer, ValuerSerializer, InstituteSerializer, PasswordResetEmailSerializer,
    PasswordResetCodeSerializer, 
)
from .validators import ValidityError
from .models import Customer


def password_reset_code():
    code = get_random_string(length=7)
    return code


def check_for_email(email):
    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return True
    return False


def sign_token():
    token = TimestampSigner(salt='extra')
    return token


def generate_safe_token(email):
    signer = sign_token().sign(email)
    return signer


def validate_contact_number(number):
    get_number = get_user_model().objects.filter(contact_number=number)
    if get_number.exists():
        raise ValidityError({'message': 'number exist', 'res': False, 'reason':
            'number assoicated with an account already'})
    else:
        return number


class CustomerSignUpAPIView(CreateAPIView):
    serializer_class = CustomerSerializer
    queryset = get_user_model()

    def create(self, request, *args, **kwarg):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if validate_contact_number(serializer.validated_data['user']['contact_number']):
                self.perform_create(serializer)
                email = serializer.validated_data['user']['email']
                request.session['email'] = email
                request.session.set_expiry(5400)
                token = generate_safe_token(email)
                return Response({'message': 'True', 'res': True, 'reason': 'signed up successfully','token': token}, status=status.HTTP_200_OK) 
            else:
                return Response({'message': 'True', 'res': True, 'reason': 'number assoicated with an account already',
                                }, status=status.HTTP_200_OK)
    

        else:
            return Response({'message': 'false', 'res': False, 'reason': 'Email already exist'},
                            status=status.HTTP_200_OK)


class PropertyOwnerSignUpAPIView(CreateAPIView):
    serializer_class = PropertyOwnerSerializer
    queryset = get_user_model()

    def create(self, request, *args, **kwargs):
        
    

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if validate_contact_number(serializer.validated_data['user']['contact_number']):
                self.perform_create(serializer)
                email = serializer.validated_data['user']['email']
                request.session['email'] = email
                request.session.set_expiry(5400)
                token = generate_safe_token(email)
                return Response({'message': 'True', 'res': True, 'reason': 'signed up successfully',
                                 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'false', 'res': False, 'reason': 'Number exist already'},
                            status=status.HTTP_200_OK)
                            
        else:
            return Response({'message': 'false', 'res': False, 'reason': serializer.errors},
                            status=status.HTTP_200_OK)

    def mail_site_admins(self):
        pass

    def mail_created_user(self):
        pass


class AgentSignUpAPIView(PropertyOwnerSignUpAPIView):
    serializer_class = AgentSerializer
    queryset = get_user_model()
  

class DeveloperSignUpAPIView(PropertyOwnerSignUpAPIView):
    serializer_class = DeveloperSerializer
    queryset = get_user_model()


class SupplierSignUpAPIView(PropertyOwnerSignUpAPIView):
    queryset = get_user_model()
    serializer_class = SupplierSerializer


class ValuerSignUpAPIView(PropertyOwnerSignUpAPIView):
    serializer_class = ValuerSerializer
    queryset = get_user_model()


class InstituteSignUpAPIView(PropertyOwnerSignUpAPIView):
    serializer_class = InstituteSerializer
    queryset = get_user_model()


class GovernmentSignUpAPIView(PropertyOwnerSignUpAPIView):
    serializer_class = GovernmentSerializer
    queryset = get_user_model()


class HotelierSignUpAPIView(PropertyOwnerSignUpAPIView):
    serializer_class = HotelierSerializer
    queryset = get_user_model()


class ValidateNumberAPIView(GenericAPIView):

    serializer_class = OtpSerializer

    auth = Auth()
    
    #permission_classes = (ValidateUser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        email_token = request.query_params.get('token', '')
        email = request.session.get('email', None)
        token = request.session.get('token', None)

        if email_token != '':
            return self.token_validation(serializer, email_token)

        elif email is not None:
            request.session['user_otp'] = email
        
            return self.process_number_validation(serializer, email)
        elif token:
            request.session['user_otp'] = email
            return self.process_number_validation(serializer, token)

        else:
            raise ValidityError({'res': False, 'message': 'False',  'reason': 'No Token'})

    def token_validation(self, serializer, token):
        try:
            safe_token = sign_token().unsign(token, max_age=5400)
        except (BadSignature, SignatureExpired):
            raise ValidityError({'res': False, 'message': 'expired token', 'reason': 'invalid token'})
        else:
            
            return self.process_number_validation(serializer, token)

    def process_number_validation(self, serializer, user_id):
        if serializer.is_valid():
            user_email_validation = self.validate_email(user_id)
            return self.perform_number_validation(user_email_validation, serializer)

    def perform_number_validation(self, user_id, serializer):
        verify_code = self.auth.verify_code(user_id, serializer.validated_data['otp_code'])
        if verify_code.ok():
            self.update_user(user_id)
            return Response({'message': 'True', 'res': True, 'reason': 'code verified successfully'},
            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'False', 'res': False, 'reason': 'Invalid Code'},
            status=status.HTTP_200_OK)

    def validate_email(self, email):
        try:
            user = get_user_model().objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            raise ValidityError({'message': 'False', 'res': False, 'reason': 'failed to verify code'})
        else:
            auth_id = user.authy_id
            return auth_id

    @staticmethod
    def update_user(instance):
        user = get_user_model().objects.filter(authy_id__iexact=instance).update(phone_number=True)
        return user


class ResendOTPTokenView(GenericAPIView):
    auth = Auth()

    def get(self, request):
        token = request.query_params.get('token', None)
        reset_token = request.query_params.get('reset_token', None)

        if token is not None:
            return self.token_validation(token)

        elif reset_token:
            return self.token_validation(reset_token)

    def token_validation(self, token):
        try:
            safe_token = sign_token().unsign(token, max_age=5400)
        except (BadSignature, SignatureExpired):
            raise ValidityError({'res': False, 'message': 'expired token', 'reason': 'invalid token'})
        else:
            tokenize = self.get_user_auth_id(safe_token)
            return self.send_otp_code(tokenize, token)

    def send_otp_code(self, number, token):
        send_code = self.auth.send_code(number)
        if send_code.ok():
            if isinstance(token, str):
                self.request.session['token'] = token
                return Response({'message': 'True', 'reason': 'code sent succesfully', 'res': True})
        else:
            return Response({'message': 'code not sent', 'reason': 'Failed to send code', 'res': False})

    @staticmethod
    def get_user_auth_id(email):
        try:
            user = get_user_model().objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            pass
        else:
            return user.authy_id
    

class ResendOTPAPIView(GenericAPIView):
    auth = Auth()
    #permission_classes = (ValidateResendOTP,)

    def get(self, request):
        email = request.session.get('user_otp', None)
        auth_id = request.session.get('otp_data', None)
        user = request.session.get('email', None)
        
        if email is not None:
            return self.validate_email(email)
    
        elif auth_id:
            return self.process_sending_code(auth_id)
            
        else:
            raise ValidityError({'error': 'an error occured'})

    def validate_email(self, email):
        try:
            user = get_user_model().objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            raise ValidityError({'message': 'False', 'res': False, 'reason': 'failed to send code'})
        else:
            auth_id = user.authy_id
            return self.process_sending_code(auth_id)

    def process_sending_code(self, user_id):
        send_otp_code = self.auth.send_code(user_id)
        if send_otp_code.ok():
            return Response({'res': True, 'message': 'True', 'reason': 'code was sent successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'False', 'res': False, 'reason': 'failed to send code' }, status=status.HTTP_200_OK)


class PasswordResetNumberAPIView(GenericAPIView):
    model = get_user_model()
    serializer_class = PasswordResetNumberSerializer

    auth = Auth()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = self.validate_number(serializer.validated_data['number'])
            send_sms = self.auth.send_code(data)
            if send_sms.errors():
                return Response({'message': 'False', 'res': False, 'reason': 'failed  send code'}, status=status.HTTP_200_OK)
            else:
                request.session['otp_data'] = data
                request.session.set_expiry(5400)
                token = generate_safe_token(data)
                return Response({'message': 'True', 'res': True, 'reason': 'code sent successfully', 'token': token}, status=status.HTTP_200_OK)
                
        else:
            return Response({'message': 'invalid payload', 'reason': 'error occured', 'res': False}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def validate_number(data):
        try:
            user = get_user_model().objects.get(contact_number=data)
        except ObjectDoesNotExist:
            raise ValidityError({'reason': 'This number does not belong to any account', 'res': False, 'message': 'number not found'})
        else:
            return user.authy_id

    
class PasswordRestEmailAPIView(GenericAPIView):
    serializer_class = PasswordResetEmailSerializer
    queryset = get_user_model()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validate_email = self.check(serializer.validated_data['email'])
            code = password_reset_code()
            message_body = 'Real Estate password reset code {}'.format(code)
            mail = send_mail('Password reset code', message_body, settings.EMAIL_HOST_USER, [serializer.validated_data['email']], fail_silently=False)
            if mail:
                tokenize_code = generate_safe_token(code)
                request.session['email_code'] = tokenize_code
                request.session.set_expiry(5400)
                request.session['user'] = validate_email
                request.session.set_expiry(5400)
                return Response({'res': True, 'message': 'True', 'reason': 'Mail sent successfully', 'token': tokenize_code,
                'email': validate_email}, status=status.HTTP_200_OK)
            else: 
                return Response({'res': False, 'message': 'False', 'reason': 'Failed to send mail'}, status=status.HTTP_200_OK)
        else:
            return Response({'res': False, 'message': 'Email does not exist', 'reason': 'Invalid Email'},  status=status.HTTP_200_OK)
    
    @staticmethod
    def check(instance):
        user = get_user_model().objects.filter(email__iexact=instance)
        if not user.exists():
            raise ValidityError({'res': False, 'message': 'not found', 'reason': 'Email doesnt belong to any account'})
        else:
            return instance


class ResendEmailCodeAPIView(GenericAPIView):
    # permission_classes = (ValidateEmailResendCode,)

    def get(self, request):
        user = request.session.get('user', None)

        if user is not None: 
            code = password_reset_code()
            message_body = 'Real Estate password reset code {}'.format(code)
            mail = send_mail('Password reset code', message_body, settings.EMAIL_HOST_USER, [user], fail_silently=False)
            if mail:
                tokenize_code = generate_safe_token(code)
                request.session['email_code'] = tokenize_code
                request.session['user'] = user
                return Response({'res': True, 'message': 'True', 'reason': 'Mail sent successfully', 'token': tokenize_code}, status=status.HTTP_200_OK)
            else: 
                return Response({'res': False, 'message': 'False', 'reason': 'Failed to send mail'}, status=status.HTTP_200_OK)
        else:
            user = request.query_params.get('email', '')
            if user == '':
                return Response({'res': False, 'message': 'False', 'reason': 'Failed to send mail'}, status=status.HTTP_200_OK)

            code = password_reset_code()
            message_body = 'Real Estate password reset code {}'.format(code)
            mail = send_mail('Password reset code', message_body, settings.EMAIL_HOST_USER, [user], fail_silently=False)
            if mail:
                tokenize_code = generate_safe_token(code)
                request.session['email_code'] = tokenize_code
                request.session['user'] = user
                return Response({'res': True, 'message': 'True', 'reason': 'Mail sent successfully', 'token': tokenize_code,
                'email': user}, status=status.HTTP_200_OK)
            else: 
                return Response({'res': False, 'message': 'False', 'reason': 'Failed to send mail'}, status=status.HTTP_200_OK)
            


class ConfirmedEmailCodeAPIView(GenericAPIView):
    serializer_class = PasswordResetCodeSerializer
    #permission_classes = (ValidateEmailCode,)

    def post(self, request):
        code = request.session.get('email_code', None)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() and code:
            check_token = self.validate_code(code)
            if check_token == serializer.validated_data['code']:
                del request.session['email_code']
                return Response({'res': True, 'message': 'True', 'reason': 'Validated code successfulluy'}, status=status.HTTP_200_OK)
            else: 
                return Response({'res': False, 'message': 'False', 'reason': 'Invalid code'}, status=status.HTTP_200_OK)
        else:
            code = request.query_params.get('token', '')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid() and code:
                token = self.validate_code(code)
                if token == serializer.validated_data['code']:
                    return Response({'res': True, 'message': 'True', 'reason': 'Validated code successfulluy'}, status=status.HTTP_200_OK)
                else: 
                    return Response({'res': False, 'message': 'False', 'reason': 'Invalid code'}, status=status.HTTP_200_OK)

    def validate_code(self, code):
        try:
            safe_token = sign_token().unsign(code, max_age=5400)
        except (BadSignature, SignatureExpired):
            raise ValidityError({'res': False, 'message': 'expired token', 'reason': 'invalid code'})
        else:
            tokenize = safe_token
            return tokenize


class PasswordResetOTPConfirmedAPIView(GenericAPIView):
    serializer_class = OtpSerializer
    permission_classes = (ValidateSession,)
    auth = Auth()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['otp_code']
            data = request.session.get('otp_data', None)
            verify_otp = self.auth.verify_code(data, code)
            if verify_otp.errors():
                return Response({'reason': 'failed to validate otp code', 'message': 'False', 'res':False})
            else:
                del request.session['otp_data']
                request.session['email_data'] = data
                return Response({'res': True, 'reason': 'code verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'False', 'reason': 'error occured', 'res': False}, status=status.HTTP_200_OK)
            
    
class PasswordResetConfirmAPIView(GenericAPIView):

 #   permission_classes = (ValidateResetPass,)
    serializer_class = PasswordResetSerializer

    def post(self, request):
        number = request.session.get('email_data', None)
        if number is None:
            email = request.session.get('user', None)
            if email is not None:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    self.change_password_with_email(email, serializer.validated_data['password'])
                    del request.session['user']
                    return Response({'message': 'True','reason': 'password changed successfully', 'res': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Failed', 'res': False,  'reason': 'Invalid password'}, status=status.HTTP_200_OK)
            else:
                email = request.query_params.get('email')
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    self.change_password_with_email(email, serializer.validated_data['password'])
                    return Response({'message': 'True','reason': 'password changed successfully', 'res': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Failed', 'res': False,  'reason': 'Invalid password'}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.change_password_with_auth(number, serializer.validated_data['password'])
                del request.session['email_data']
                return Response({'message': 'True','reason': 'password changed successfully', 'res': True}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed', 'res': False,  'reason': 'Invalid password'}, status=status.HTTP_200_OK)

    def change_password_with_auth(self, instance, password):
        try:
            queryset = get_user_model().objects.get(authy_id__iexact=instance)
        except ObjectDoesNotExist:
            raise ValidityError({'reason': 'unable to change password', 'message': 'False', 'res': False})
        else:
            queryset.password = password
            queryset.set_password(password)
            queryset.save()
            return queryset

    def change_password_with_email(self, instance, password):
        try:
            queryset = get_user_model().objects.get(email__iexact=instance)
        except ObjectDoesNotExist:
            raise ValidityError({'reason': 'unable to change password', 'message': 'False', 'res': False})
        else:
            queryset.password = password
            queryset.set_password(password)
            queryset.save()
            return queryset


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    queryset = get_user_model()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is None:
                return self.user_is_invalid()

            elif user and user.is_confirmed and user.phone_number_verified:
                return self.process_login(user)

            elif user and not user.is_confirmed and not user.phone_number_verified:
                return self.process_login(user)
            
            elif user and not user.phone_number_verified:
                return self.process_login(user)
        else:
            return self.user_password_invalid()

    def user_is_invalid(self):
        return Response({'message': 'False', 'reason': 'invalid Credentials', 'res': False}, status=status.HTTP_200_OK)

    def user_password_invalid(self):
        return Response({'message': 'False', 'reason': 'invalid Password', 'res': False}, status=status.HTTP_200_OK)

    def process_login(self, user):
        return self.login_normal_user(user)

    """
    def login_user_with_no_notification(self, user):
        account = account_type(user)
        image = account_image(user)
        account_name = account_full_name(user)
        login(self.request, user=user)
        token = encode_user_payload(user)
        return Response({'token': token,
            'fullname':account_name, 'profile_image': image, 'user_id': user.pk, 'phone_number': user.contact_number,'email': user.email, 'message': 'True', 'reason': 'user account confirmed', 'res':True, 'notify_stat': False,
        'account_type': account }, status=status.HTTP_200_OK)
    
    def login_user_with_notification(self, user):
        account = account_type(user)
        image = account_image(user)
        account_name = account_full_name(user)
        
        login(self.request, user=user)
        token = encode_user_payload(user)
        return Response({'token': token, 'fullname':account_name, 'profile_image': image, 'user_id': user.pk, 'phone_number': user.contact_number, 'email': user.email, 'account_type': account, 'message': 'True', 'reason': 'user account confirmed', 'res':True, 'notify_stat': user.notify}, status=status.HTTP_200_OK)
    """
    def login_normal_user(self, user):
        account = account_type(user)
        account_name = account_full_name(user)
        image = account_image(user)
        login(self.request, user=user)
        token = encode_user_payload(user)
        return Response({'token': token, 'fullname': account_name, 'profile_image': image, 'user_id': user.pk, 'phone_number': user.contact_number, 'email': user.email, 'account_type': account, 'message': 'True', 'reason': 'user account confirmed', 
        'res':True, 
         'notify_stat': user.notify}, status=status.HTTP_200_OK)



class LogoutAPIView(GenericAPIView):

    permission_classes = (JwtAuthentication,)

    def get(self, request):
        logout(request)
        return Response({'message': 'True', 'reason': 'logged out successfully', 'res':True}, status=status.HTTP_200_OK)


class ReconfirmAccountNumberAPIView(GenericAPIView):
    permission_classes = (JwtAuthentication,)
    auth = Auth()

    def get(self, request):
        self.auth.send_code(request.user.authy_id)
        return Response({'res': True, 'message': True, 'reason': 'A verification code was sent'})


class ReconfirmAccountNumberValidationAPIView(GenericAPIView):
    permission_classes = (JwtAuthentication,)
    serializer_class = OtpSerializer
    auth = Auth()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            check_valid_code = self.auth.verify_code(request.user.authy_id, serializer.validated_data['otp_code'])
            if check_valid_code.ok():
                self.update_user_phone_status()
                return Response({'message': 'True', 'res': True, 'reason': 'Phone number confirmed'})
            else:
                return Response({'message': 'False',  'res': False, 'reason': 'Invalid code'})

    def update_user_phone_status(self):
        return get_user_model().objects.filter(email__iexact=self.request.user).update(phone_number=True)



class VerificationAPIView(APIView):

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        auth_code = request.query_params.get('auth_code',  None)

        if email is  None and auth_code is  None:
            raise ValidityError({
                'res': False,
                'message': 'no paramaters provided',
                'reason':  'No paramaters specified in request'

            })

        else:
            self.send_mail(email, auth_code)
            return Response({
                'res': True,
                'message': 'code sent',
                'reason': 'The auth code was sent'
            })
            
        
    def send_mail(self, email, code):
        message = 'Your auth_code is {} '.format(code)
        return send_mail('Auth verification code', message, settings.EMAIL_HOST_USER, recipient_list=[email])
