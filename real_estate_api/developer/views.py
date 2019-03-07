from django.shortcuts import render

# Create your views here.
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
RetrieveDestroyAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from .models import DeveloperListing
from .serializer import DeveloperSerializer
from .permission import IsDeveloper
from accounts.authentication import JwtAuthentication

from rest_framework.permissions import IsAuthenticated
from owner.views import PropertyListingCreateAPIView



class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsDeveloper
    
    )
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = DeveloperListing
    serializer_class = DeveloperSerializer

 

class RetrieveHotelPost(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsDeveloper
    
    )
    authentication_classes = (JwtAuthentication, SessionAuthentication)

    queryset = DeveloperListing
    serializer_class = DeveloperSerializer
    lookup_url_kwarg = 'pk'



class DeleteHotelPost(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsDeveloper
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = DeveloperListing
    serializer_class = DeveloperSerializer
    lookup_url_kwarg = 'pk'

class ListHotelPost(ListAPIView):
    permission_classes = (IsAuthenticated, IsDeveloper
    
    ,)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = DeveloperListing
    serializer_class = DeveloperSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(developer_id=user).all()
