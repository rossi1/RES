from rest_framework.serializers import ModelSerializer

from .models import DeveloperListing

class DeveloperSerializer(ModelSerializer):
    class Meta:
        model = DeveloperListing
        exclude = ['pub_date', 'developer_id']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if hasattr(request, 'user') and request is not None:
            user = request.user

            create = DeveloperListing.objects.create(developer_id=user, 
  
            **validated_data)
            return create