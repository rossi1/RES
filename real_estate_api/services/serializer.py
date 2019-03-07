from rest_framework.serializers import ModelSerializer
from accounts.models  import ServicesInfo

from .models import ServicesListing

class ServicesSerializer(ModelSerializer):
    class Meta:
        model = ServicesListing
        exclude = ['pub_date', 'services_id', 'order_uuid']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if hasattr(request, 'user') and request is not None:
            user = request.user
            data = self.get_services_info(user)
            
            create = ServicesListing.objects.create(services_id=user, 
            location=data['location'],
            order_uuid=data['order_id'],
                **validated_data)
                
            return create

    def get_services_info(self, data):
        try:
            user = ServicesInfo.objects.get(user=data)
        except ServicesInfo.DoesNotExist:
            pass
        else:
            return {
                
                'order_id': user.order_id,
                'location': user.location
            }
        