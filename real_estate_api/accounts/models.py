from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings



from rest_framework import exceptions

import cloudinary

from .managers import UserManager
from .utils import Auth


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=120, unique=True)
    authy_id = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    is_confirmed = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=250)
    is_property_owner = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)
    is_government = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_hotelier = models.BooleanField(default=False)
    is_valuer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    notify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @staticmethod
    def send_otp_code(authy_id):
        auth = Auth()
        if hasattr(auth, 'send_code'):
            send_sms = auth.send_code(authy_id)
            if send_sms.errors():
                raise exceptions.ValidationError({'detail': 'failed to send otp code'})
            else:
                return send_sms


class SignUPInfo(models.Model):
    full_name = models.CharField(max_length=250)
    cac_number = models.IntegerField()
    office_address = models.CharField(max_length=250)
    work_identity = cloudinary.models.CloudinaryField('image')
    profile_picture = cloudinary.models.CloudinaryField('images', default='/avatar/customer.png')
    latitude = models.FloatField()
    service_type = models.CharField(max_length=250, default='')
    longitude = models.FloatField()
    location = models.PointField(null=True, geography=True)
    

    def save(self, *args, **kwargs):
        self.location = GEOSGeometry('POINT({} {})'.format(self.longitude, self.latitude))
        super().save(*args,**kwargs)

    
    class Meta:
        abstract = True

class HotelInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotelier')
    cac_number = models.IntegerField(unique=True)
    hotel_website = models.URLField(unique=True, blank=True)
    address  = models.CharField(max_length=250)
    hotel_name  = models.CharField(max_length=250, default='')
    city  = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    order_id = models.IntegerField(unique=True, default=0)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(null=True, geography=True)
    work_identity = cloudinary.models.CloudinaryField('image')
    hotel = cloudinary.models.CloudinaryField('image')
    profile_picture = cloudinary.models.CloudinaryField('images', default='/avatar/customer.png')

    
    def save(self, *args, **kwargs):
        self.location = GEOSGeometry('POINT({} {})'.format(self.longitude, self.latitude))
        super().save(*args, **kwargs)
    

    def __str__(self):
        return str(self.user)


class PropertyOwnerInfo(models.Model):
    GENDER_CHOICE = (('male', 'male'),
                     ('female', 'female'))

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    full_name = models.CharField(max_length=250)
    contact_address = models.CharField(max_length=250)
    profile_picture = cloudinary.models.CloudinaryField('images', default='/avatar/customer.png')
    gender = models.CharField(max_length=250)

    def __str__(self):
        return str(self.user)
    

class AgentInfo(SignUPInfo):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent')

    def __str__(self):
        return str(self.user)


class DeveloperInfo(SignUPInfo):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='developer')

    def __str__(self):
        return str(self.user)


class GovernmentInfo(SignUPInfo):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='government')


class Institute(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='institute')
    institute_name = models.CharField(max_length=250)
    institute_address = models.CharField(max_length=250)
    cac_number = models.CharField(max_length=250)
    work_identity = cloudinary.models.CloudinaryField('images')
    website = models.URLField(blank=True)
    profile_picture = cloudinary.models.CloudinaryField('images', default='/avatar/customer.png')

    def __str__(self):
        return str(self.user)


class Valuer(SignUPInfo):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='valuer')

    def __str__(self):
        return str(self.user)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    full_name = models.CharField(max_length=250)
    contact_address = models.CharField(max_length=150, blank=True)
    profile_picture = cloudinary.models.CloudinaryField('images', default='/avatar/customer.png')

    def __str__(self):
        return str(self.user)


class Supplier(SignUPInfo):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='supplier')

    def __str__(self):
        return str(self.user)


class Estate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    description = models.TextField()
    topic = models.CharField(max_length=250)
    document = models.FileField()
    
    def __str__(self):
        return str(self.user)


class ServicesInfo(SignUPInfo):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='services_idp')
    order_id = models.IntegerField(unique=True, default=0)
    def __str__(self):
        return str(self.user)



