from rest_framework.permissions import IsAuthenticated

from owner.views import (PropertyListingCreateAPIView, ListPropertyAPIView, 
UpdatePropertyAPIView, DeletePropertyAPIView)



from .permission import IsAgent

from accounts.permission import JwtAuthentication

class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (JwtAuthentication, IsAuthenticated)


class RetrieveHotelPost(UpdatePropertyAPIView):
    permission_classes = (JwtAuthentication, IsAuthenticated)


class DeleteHotelPost(DeletePropertyAPIView):
    permission_classes = (JwtAuthentication, IsAuthenticated)

class ListHotelPost(ListPropertyAPIView):
    permission_classes = (JwtAuthentication, IsAuthenticated)

  
