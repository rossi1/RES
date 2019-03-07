from rest_framework.serializers import ModelSerializer

from .models import GovermentListing

class GovernmentSerializer(ModelSerializer):
    class Meta:
        model = GovermentListing
        exclude = ['pub_date', 'government_id']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if hasattr(request, 'user') and request is not None:
            user = request.user
          
        
            create = GovermentListing.objects.create(government_id=user, 
         
            **validated_data)
            return create