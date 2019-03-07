from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from owner.models import PropertyListing, LandListing
from accounts.models import HotelInfo, ServicesInfo, Supplier
from hotel.models  import HotelListing
from supplier.models import SupplierListing
from professional.models import ProfessionalListing
from services.models import ServicesListing


class PropertySerializer(ModelSerializer):
    class Meta:
        model = PropertyListing
        exclude = ('location', 'latitude', 'longitude')


class Hotel(ModelSerializer):
    class Meta:
        model = HotelInfo
        exclude = ('user', 'latitude', 'longitude', 'work_identity', 'profile_picture',
        'cac_number')


class HotelSerializer(ModelSerializer):
    class Meta:
        model = HotelListing
        exclude = ('website', 'hotel_name',  'listing_id', 'address',
        'city', 'order_uuid',
        'state',
        )

class LandSerializer(ModelSerializer):
    class Meta:
        model = LandListing
        exclude = ('location', 'latitude', 'longitude')


class ProfessionalSerializer(ModelSerializer):
    class Meta:
        model = ProfessionalListing
        exclude = ('location', 'latitude', 'longitude')



class SupplierSerializer(ModelSerializer):
    class Meta:
        model = SupplierListing
        exclude = ('location', 'latitude', 'longitude')


class ServicesSerializer(ModelSerializer):
    class Meta:
        model = ServicesInfo
        exclude = ('location',)

class ServicesInfoSerializer(ModelSerializer):
    class Meta:
        model = ServicesListing
        fields = '__all__'

class SupplierInfo(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ('full_name', 'office_address', 'profile_picture')

