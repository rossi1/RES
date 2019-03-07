from rest_framework import serializers
from accounts.models import Supplier

from .models import SupplierListing


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SupplierListing
        exclude = ('listing_id', 'location')

    
    def create(self, validated_data):
        user = None
        request = self.context.get('request', None)
        data = self.get_services_info(user)
        
        if request and hasattr(request, 'user'):
            user = request.user
            supplier = SupplierListing.objects.create(listing_id=user,
            location = data['location']
            **validated_data)
            return supplier


    def get_services_info(self, data):
        try:
            user = Supplier.objects.get(user=data)
        except Supplier.DoesNotExist:
            pass
        else:
            return {
                
               
                'location': user.location
            }
        