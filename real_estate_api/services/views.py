from django.shortcuts import render

# Create your views here.
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
RetrieveDestroyAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from .models import ServicesListing
from .serializer import ServicesSerializer
from .permission import IsServices
from accounts.authentication import JwtAuthentication

from rest_framework.permissions import IsAuthenticated
from owner.views import PropertyListingCreateAPIView



class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsServices
    
    )
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = ServicesListing
    serializer_class = ServicesSerializer

 

class RetrieveHotelPost(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsServices
    
    )
    authentication_classes = (JwtAuthentication, SessionAuthentication)

    queryset = ServicesListing
    serializer_class = ServicesSerializer
    lookup_url_kwarg = 'pk'



class DeleteHotelPost(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsServices
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = ServicesListing
    serializer_class = ServicesSerializer
    lookup_url_kwarg = 'pk'

class ListHotelPost(ListAPIView):
    permission_classes = (IsAuthenticated, IsServices
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = ServicesListing
    serializer_class = ServicesSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(services_id=user).all()
