from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError


from owner.utils import get_latlng

from .models import ProfessionalListing


class ProfessionalSerializer(ModelSerializer):
    class Meta:
        model = ProfessionalListing
        exclude = ('listing_id',)
    
    
    def create(self, validated_data):
        address = validated_data.pop('brand_address')
        city = validated_data.pop('city')
        full_address = '{}, {}'.format(address, city)
        request = self.context.get('request', None)
        if request is not None and hasattr(request, 'user'):
            user = request.user
            lat =  request.query_params.get('lat', '')
            long = request.query_params.get('long', '')
            image_path = validated_data.pop('images')
            #latlng = get_latlng(full_address)
            create_professional_listing = ProfessionalListing.objects.create(listing_id=user,
            address=address, city=city, **validated_data)
            return create_professional_listing
        else:
            raise ValidationError({'response': 'An error occured ', 'res': False, 'message': 'False'})
     