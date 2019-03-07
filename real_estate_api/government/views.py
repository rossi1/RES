from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
RetrieveDestroyAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from .models import GovermentListing
from .serializer import GovernmentSerializer
from .permission import IsGovernment
from accounts.authentication import JwtAuthentication

from rest_framework.permissions import IsAuthenticated
from owner.views import PropertyListingCreateAPIView



class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsGovernment
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = GovermentListing
    serializer_class = GovernmentSerializer

 

class RetrieveHotelPost(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsGovernment
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication )

    queryset = GovermentListing
    serializer_class = GovernmentSerializer
    lookup_url_kwarg = 'pk'



class DeleteHotelPost(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsGovernment
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = GovermentListing
    serializer_class = GovernmentSerializer
    lookup_url_kwarg = 'pk'

class ListHotelPost(ListAPIView):
    permission_classes = (IsAuthenticated, IsGovernment
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = GovermentListing
    serializer_class = GovernmentSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(government_id=user).all()
