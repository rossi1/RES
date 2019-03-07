import re
import random 


from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.response import Response


from .utils import Auth
from .models import (HotelInfo, PropertyOwnerInfo,
                     AgentInfo, Supplier, Valuer, Institute, GovernmentInfo,
                     DeveloperInfo, Customer, ServicesInfo)
from .validators import ValidityError


def generated_unique_id():
    ran = ''.join(str(random.randint(2, 8)) for x in range(6))
    return ran



def create_auth(email, phone):
    user = Auth()
    create = user.create_user(email, phone)
    if create.ok():
        return create.id
    elif create.errors():
        raise ValidityError({'reason': 'Invalid Phone Number', 'res': False, 'message': 'invalid number'})


def create_user(instance):
    user = get_user_model().objects.create_user(email=instance['email'],
                                                contact_number=instance['contact_number'])
    user.set_password(instance['password'])
    return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'contact_number']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    '''
    def validate_password(self, value):
        if not re.search(r"^(?=.\d)(?=.[a-z])(?=.*[A-Z]).{8,}$", value):
            raise serializers.ValidationError('invalid passphrase format')
        return value
    '''


class PropertyOwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = PropertyOwnerInfo
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_property_owner = True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            owner = PropertyOwnerInfo.objects.create(user=user, **validated_data)
            return owner


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
   
    class Meta:
        model = AgentInfo
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_agent = True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            agent = AgentInfo.objects.create(user=user, **validated_data)
            return agent


class DeveloperSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = ServicesInfo
        exclude = ('location', 'service_type','order_id')


    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_developer=True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            developer = ServicesInfo.objects.create(user=user, 
            service_type='developer',  order_id=generated_unique_id(),
            **validated_data)

            return developer


class GovernmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = ServicesInfo
        exclude = ('location', 'service_type', 'order_id')

        
    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_government=True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            government = ServicesInfo.objects.create(user=user, 
            service_type='government', order_id=generated_unique_id(),
            **validated_data)
            return government


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_customer = True
            user.is_confirmed = True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            print(create_auth_id)
            customer = Customer.objects.create(user=user, **validated_data)
            return customer

        

class SupplierSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Supplier
        exclude = ('location', 'service_type')


    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_supplier=True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            supplier = Supplier.objects.create(user=user, 
            service_type='supplier', **validated_data
            )
            return supplier


class HotelierSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = HotelInfo
        exclude = ('location', 'order_id')
        


    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])

      

        if create_auth_id:
            user =  create_user(instance=user)
            user.is_hotelier=True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            hotel_info = HotelInfo.objects.create(user=user,
            order_id=generated_unique_id(),
            **validated_data)
            return hotel_info
        
    
class InstituteSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
   
    class Meta:
        model = Institute
        fields = '__all__'
        

    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_institute=True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            institute =Institute.objects.create(user=user, **validated_data)
            
            return institute


class ValuerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = ServicesInfo
        exclude = ('location', 'service_type', 'order_id')


    def create(self, validated_data):
        user = validated_data.pop('user')
        create_auth_id = create_auth(user['email'], 
        user['contact_number'])
        if create_auth_id:
            user = create_user(instance=user)
            user.is_valuer=True
            user.authy_id = create_auth_id
            user.save()
            user.send_otp_code(create_auth_id)
            valuer = ServicesInfo.objects.create(user=user, 
            service_type='valuer',  order_id=generated_unique_id(),
            **validated_data)
            return valuer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True)

    '''
    def validate_password(self, value):
        if not re.search(r"^(?=.\d)(?=.[a-z])(?=.*[A-Z]).{8,}$", value):
            raise serializers.ValidationError('invalid passphrase format')
        return value
    '''
    

class OtpSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PasswordResetNumberSerializer(serializers.Serializer):
    number = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)

    '''
    def validate_password(self, value):
        if not re.search(r"^(?=.\d)(?=.[a-z])(?=.*[A-Z]).{8,}$", value):
            raise serializers.ValidationError('invalid passphrase format')
        return value
    '''

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PasswordResetCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

