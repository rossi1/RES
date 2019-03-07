from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from accounts.models import PropertyOwnerInfo, AgentInfo

from .models import PropertyListing, LandListing
from .utils import get_latlng


class PropertySerializer(ModelSerializer):
    class Meta:
        model = PropertyListing
        exclude = ('listing_id', 'location', 'contact_name',
        'contact_profile_photo'
                 )

    def create(self, validated_data):
        address = validated_data.pop('address')
        city = validated_data.pop('city')
        full_address = '{}, {}'.format(address, city)
        contact_number = validated_data.pop('contact_number')
        request = self.context.get('request', None)

        #user_id = self.context.get('user_id', None)

        if request is not None and hasattr(request, 'user'):
            user = request.user
            contact_info = self.get_user_photo(user)
            #latlng = get_latlng(full_address)
            #print(latlng)

            if contact_number == '': 

                create_property_listing = PropertyListing.objects.create(listing_id=user,
                                                                        city=city,
                                                                         address=address,
                                                                         contact_number=request.user.contact_number,
                                                                         contact_name=contact_info['full_name'],
                                                                         contact_profile_photo=contact_info['image'],
                                                                         **validated_data)

            else:
                create_property_listing = PropertyListing.objects.create(listing_id=user,
                                                                         city=city,
                                                                         address=address, contact_number=contact_number,
                                                                         contact_name=contact_info['full_name'],
                                                                         contact_profile_photo=contact_info['image'],
                                                                    
                                                                         **validated_data)

            return create_property_listing

    """

        elif user_id is not None:
            user_ = get_user_model().objects.get(pk=user_id)
            user = user_
           # contact_info = self.get_user_photo(user)
            latlng = get_latlng(full_address)
            print(latlng)

            if contact_number == '': 

                create_property_listing = PropertyListing.objects.create(listing_id=user, latitude=latlng.lat,
                                                                         longitude=latlng.lng, city=city,
                                                                         address=address,
                                                                         contact_number=request.user.contact_number,
                                                                         contact_name=contact_info['full_name'],
                                                                         contact_profile_photo=contact_info['image'],
                                                                         **validated_data)

            else:
                create_property_listing = PropertyListing.objects.create(listing_id=user, latitude=latlng.lat,
                                                                         longitude=latlng.lng, city=city,
                                                                         address=address, contact_number=contact_number,
                                                                    
                                                                         **validated_data)
        
        else:
            raise ValidationError(detail='failed')

    """

    def get_user_photo(self, obj):
        if obj.is_property_owner:
            try:
                info = PropertyOwnerInfo.objects.get(user=obj)
            except PropertyOwnerInfo.DoesNotExist:
                pass
            else:
                return {'full_name': info.full_name, 'image': info.profile_picture}
        else:
            try:
                info = AgentInfo.objects.get(user=obj)
            except AgentInfo.DoesNotExist:
                pass
            else:
                return {'full_name': info.full_name, 'image': info.profile_picture}



class LandSerializer(ModelSerializer):
    class Meta:
        model = LandListing
        exclude = ('listing_id', 'location',
        'contact_name',
        'contact_profile_photo'
        )

    def create(self, validated_data):
        address = validated_data.pop('address')
        city = validated_data.pop('city')
        full_address = '{}, {}'.format(address, city)
        request = self.context.get('request', None)
        #contact_info = self.get_user_photo(user)
        #user_id = self.context.get('user_id', None)

        if request is not None and hasattr(request, 'user'):
            user = request.user
            contact_info = self.get_user_photo(user)
            create_property_listing = LandListing.objects.create(listing_id=user, 
            contact_name=contact_info['full_name'],
            contact_profile_photo=contact_info['image'],**validated_data)
            return create_property_listing
       
        else:
            raise ValidationError(detail='failed')

    def get_user_photo(self, obj):
        if obj.is_property_owner:
            try:
                info = PropertyOwnerInfo.objects.get(user=obj)
            except PropertyOwnerInfo.DoesNotExist:
                pass
            else:
                return {'full_name': info.full_name, 'image': info.profile_picture}
        else:
            try:
                info = AgentInfo.objects.get(user=obj)
            except AgentInfo.DoesNotExist:
                pass
            else:
                return {'full_name': info.full_name, 'image': info.profile_picture}
