import random 
from rest_framework import serializers

from .models import HotelListing
from accounts.models import HotelInfo



def generated_unique_id():
    ran = ''.join(str(random.randint(2, 8)) for x in range(6))
    return ran




class CreateHotelPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelListing
        exclude = ('website', 'hotel_name',  'listing_id', 'address',
        'city', 'order_uuid', 'location',
        'state',
         )
    
 
    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        
        if request and hasattr(request, 'user'):
            
            user = request.user
            hotel_info = self.get_hotel_info(user)
       
         

            hotel_post = HotelListing.objects.create(listing_id=user, 
            website=hotel_info['website'],
            hotel_name=hotel_info['hotel_name'],
            address=hotel_info['address'],
            state=hotel_info['state'],
            city=hotel_info['city'],
            location=hotel_info['location'],
            order_uuid=hotel_info['order_id'],

            **validated_data)
            return hotel_post

    def get_hotel_info(self, data):
        try:
            user = HotelInfo.objects.get(user=data)
        except HotelInfo.DoesNotExist:
            pass
        else:
            return {
                'website': user.hotel_website,
                'address': user.address,
                'city': user.city,
                'hotel_name': user.hotel_name,
                'state':user.state,
                'location': user.location,
                'order_id': user.order_id
            }
        

    
   


