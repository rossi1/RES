from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
RetrieveDestroyAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from .models import ValuerListing
from .serializer import ValuerSerializer
from .permission import IsValuer
from accounts.authentication import JwtAuthentication

from rest_framework.permissions import IsAuthenticated
from owner.views import PropertyListingCreateAPIView



class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsValuer
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = ValuerListing
    serializer_class = ValuerSerializer

 

class RetrieveHotelPost(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsValuer
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)

    queryset = ValuerListing
    serializer_class = ValuerSerializer
    lookup_url_kwarg = 'pk'



class DeleteHotelPost(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsValuer
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = ValuerListing
    serializer_class = ValuerSerializer
    lookup_url_kwarg = 'pk'

class ListHotelPost(ListAPIView):
    permission_classes = (IsAuthenticated, IsValuer
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = ValuerListing
    serializer_class = ValuerSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(valuer_id=user).all()
