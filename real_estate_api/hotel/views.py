
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import HotelListing
from .serializer import CreateHotelPostSerializer
from accounts.authentication import JwtAuthentication
from .permission import IsHotel
from owner.views import PropertyListingCreateAPIView, ListPropertyAPIView, UpdatePropertyAPIView, DeletePropertyAPIView

class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsHotel) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = HotelListing
    serializer_class = CreateHotelPostSerializer

class RetrieveHotelPost(UpdatePropertyAPIView):
    permission_classes = (IsAuthenticated, IsHotel) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = HotelListing
    serializer_class = CreateHotelPostSerializer
    lookup_url_kwarg = 'pk'


class DeleteHotelPost(DeletePropertyAPIView):
    permission_classes = (IsAuthenticated, IsHotel) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = HotelListing
    serializer_class = CreateHotelPostSerializer
    lookup_url_kwarg = 'pk'


class ListHotelPost(ListPropertyAPIView):
    permission_classes = (IsAuthenticated,IsHotel) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = HotelListing
    serializer_class = CreateHotelPostSerializer
