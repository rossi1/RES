import os
import jwt
from datetime import timedelta, datetime


from django.conf import settings

from authy.api import AuthyApiClient

class Auth:
    auth = AuthyApiClient(settings.API_KEY)

    def create_user(self, email, phone, code=234):
        create = self.auth.users.create(email=email, phone=phone, country_code=code)
        return create

    def send_code(self, auth_id):
        sms_code = self.auth.users.request_sms(auth_id, {'force': True})
        return sms_code


    def verify_code(self, auth_id, token):
        verify_code = self.auth.tokens.verify(auth_id, token, {'force': True})
        return verify_code



def account_type(user):
    account_type = None

    if user.is_agent:
        account_type = 'Agent'
    elif user.is_customer:
        account_type = 'Customer'
    elif user.is_developer:
        account_type = 'Developer'
    elif user.is_institute:
        account_type = 'Institution'
    elif user.is_government:
        account_type = 'Government'
    elif user.is_hotelier:
        account_type = 'Hotelier'
    elif user.is_supplier:
        account_type = 'Supplier'
    elif user.is_property_owner:
        account_type = 'Owner'
    elif user.is_valuer:
        account_type = 'Valuer'
        
    return account_type


def account_image(user):
    account_image = None
    
    if user.is_agent:
        account_image = user.agent.profile_picture.url 
    elif user.is_customer:
        account_image = user.customer.profile_picture.url

    elif user.is_institute:
        account_image = user.institute.profile_picture.url
    elif user.is_hotelier:
        account_image = user.hotelier.profile_picture.url
    elif user.is_supplier:
        account_image = user.supplier.profile_picture.url
    elif user.is_property_owner:
        account_image = user.owner.profile_picture.url
    else:
        account_image = user.services_idp.profile_picture.url
   
        
    return account_image
    
def account_full_name(user):
    account_name = None
    
    if user.is_agent:
        account_name = user.agent.full_name
    elif user.is_customer:
        account_name = user.customer.full_name
    elif user.is_institute:
        account_name= user.institute.institute_name
    elif user.is_hotelier:
        account_name = user.hotelier.hotel_name
    elif user.is_supplier:
        account_name = user.supplier.profile_picture.url
    elif user.is_property_owner:
        account_name = user.owner.full_name
    else:
        account_name = user.services_idp.full_name

    return account_name


def encode_user_payload(user):
    payload = {
        'user': user.email ,
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_DELTA_MINTUES)
    }
    jwt_token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    return jwt_token.decode('utf-8')