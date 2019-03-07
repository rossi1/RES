from rest_framework.serializers import ModelSerializer

from .models import GovermentListing

class InstituteSerializer(ModelSerializer):
    class Meta:
        model = InstituteListing
        exclude = ['pub_date', 'government_id']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if hasattr(request, 'user') and request is not None:
            user = request.user
            create = InstitueListing.objects.create(institute_id=user, **validated_data)
            return create