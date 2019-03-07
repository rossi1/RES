from rest_framework.serializers import ModelSerializer

from .models import ValuerListing

class ValuerSerializer(ModelSerializer):
    class Meta:
        model = ValuerListing
        exclude = ['pub_date', 'valuer_id']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if hasattr(request, 'user') and request is not None:
            user = request.user
            create = ValuerListing.objects.create(valuer_id=user, **validated_data)
            return create