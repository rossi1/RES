from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
RetrieveDestroyAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import SupplierListing
from .serializer import SupplierSerializer
from .permission import IsSupplier

from accounts.authentication import JwtAuthentication
from owner.views import PropertyListingCreateAPIView

class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsSupplier) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = SupplierListing
    serializer_class = SupplierSerializer

class RetrieveHotelPost(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsSupplier) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = SupplierListing
    serializer_class = SupplierSerializer
    lookup_url_kwarg = 'pk'



class DeleteHotelPost(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsSupplier) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = SupplierListing
    serializer_class = SupplierSerializer
    lookup_url_kwarg = 'pk'

class ListHotelPost(ListAPIView):
    permission_classes = (IsAuthenticated, IsAuthenticated) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = SupplierListing
    serializer_class = SupplierSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(listing_id=user).all()
