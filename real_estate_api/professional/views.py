
from owner.views import (PropertyListingCreateAPIView, ListPropertyAPIView, 
UpdatePropertyAPIView, DeletePropertyAPIView)

from .models import ProfessionalListing
from .serializer import ProfessionalSerializer
from accounts.permission import JwtAuthentication


class ProfessionalCreateAPIVIew(PropertyListingCreateAPIView):
    permission_classes = (JwtAuthentication,)
    queryset = ProfessionalListing
    serializer_class = ProfessionalSerializer


class ListProfessionalServiceAPIView(ListPropertyAPIView):
    permission_classes = (JwtAuthentication,)
    queryset = ProfessionalListing
    serializer_class = ProfessionalSerializer


class UpdateProfessionalServiceAPIView(UpdatePropertyAPIView):
    permission_classes = (JwtAuthentication,)
    queryset = ProfessionalListing
    serializer_class = ProfessionalSerializer


class DeleteProfessionalAPIView(DeletePropertyAPIView):
    permission_classes = (JwtAuthentication,)
    queryset = ProfessionalListing
    serializer_class = ProfessionalSerializer