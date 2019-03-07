from rest_framework import serializers

from accounts.models import Estate

class UserPortFolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = getattr(request, 'user')
        return Estate.objects.create(user=user, **validated_data)
