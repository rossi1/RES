from django.shortcuts import render

# Create your views here.
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView,
RetrieveDestroyAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from .models import InstituteListing
from .serializer import InstituteSerializer
from .permission import IsInstitute
from accounts.authentication import JwtAuthentication

from rest_framework.permissions import IsAuthenticated
from owner.views import PropertyListingCreateAPIView



class CreateHotelPost(PropertyListingCreateAPIView):
    permission_classes = (IsAuthenticated, IsInstitute
    
    )
    authentication_classes = (JwtAuthentication, )
    queryset = InstituteListing
    serializer_class = InstituteSerializer

 

class RetrieveHotelPost(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsInstitute
    
    )
    authentication_classes = (JwtAuthentication, )

    queryset = InstituteListing
    serializer_class = InstituteSerializer
    lookup_url_kwarg = 'pk'



class DeleteHotelPost(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsInstitute
    
    ,)
    authentication_classes = (JwtAuthentication, )
    queryset = InstituteListing
    serializer_class = InstituteSerializer
    lookup_url_kwarg = 'pk'

class ListHotelPost(ListAPIView):
    permission_classes = (IsAuthenticated, IsInstitute
    
    ,)
    authentication_classes = (JwtAuthentication, )
    queryset = InstituteListing
    serializer_class = InstituteSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(institute_id=user).all()
