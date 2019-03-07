from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import PropertyListing, LandListing

from .serializer import PropertySerializer, LandSerializer
from .permission import IsValidUser, CanPostListing

from accounts.authentication import JwtAuthentication


class PropertyListingCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsValidUser) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = PropertyListing
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        context = {
            'request': request.user,
            'user_id': request.query_params.get('user_id')
        }

        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'reason': 'created successfully', 'res': True, 'message': 'True'}, status=status.HTTP_200_OK)
        else:
            return Response({'reason': serializer.errors, 'res': False, 'message': 'False'}, status=status.HTTP_200_OK)

   
    
    
    
class LandListingCreateAPIView(PropertyListingCreateAPIView):
    queryset = LandListing
    serializer_class = LandSerializer


class ListPropertyAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsValidUser) #, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    queryset = PropertyListing
    serializer_class = PropertySerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.objects.filter(listing_id=user).all()


class ListLandAPIView(ListPropertyAPIView):
    queryset = LandListing
    serializer_class = LandSerializer

    
class UpdatePropertyAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsValidUser) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    serializer_class = PropertySerializer
    queryset = PropertyListing
    lookup_url_kwarg = 'pk'


class UpdateLandAPIView(UpdatePropertyAPIView):
    serializer_class = LandSerializer
    queryset = LandListing


class DeletePropertyAPIView(DestroyAPIView):
    queryset = PropertyListing
    serializer_class = PropertySerializer
    permission_classes = (IsAuthenticated, IsValidUser) #IsValidUser, CanPostListing)
    authentication_classes = (JwtAuthentication, SessionAuthentication)
    lookup_url_kwarg = 'pk'


class DeleteLandAPIView(DeletePropertyAPIView):
    queryset = PropertyListing
    serializer_class = PropertySerializer
