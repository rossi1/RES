from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.contrib.gis.measure import D
from django.db.models import Q, Max
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters



from rest_framework.generics import (
    GenericAPIView, ListAPIView, RetrieveAPIView
    )

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


from accounts.models import Customer, AgentInfo, HotelInfo, ServicesInfo, Supplier
from accounts.validators import ValidityError
from owner.models import PropertyListing, LandListing
from supplier.models import SupplierListing
from services.models import ServicesListing
from owner.serializer import LandSerializer
from professional.models import ProfessionalListing
#from professional.serializer import ProfessionalSerializer
from hotel.models import HotelListing
from hotel.serializer import CreateHotelPostSerializer

from .permission import IsCustomer, IsSignUp, CanViewListing
from .serializer import (PropertySerializer, HotelSerializer,
LandSerializer, SupplierSerializer,
 ProfessionalSerializer, ServicesSerializer, Hotel,
 ServicesInfoSerializer,  SupplierInfo

)





class NotificationAPIView(GenericAPIView):
    permission_classes = (IsSignUp, IsAuthenticated)

    def get(self, request):
        user = request.session.get('user_otp', None)
        if user is not None:
            get_user_model().objects.filter(email=user).update(notify=True)
            request.session.clear()
            return Response({'res': True, 'message': 'True', 'reason': 'update okay'}, status=status.HTTP_200_OK)
        else:
            get_user_model().objects.filter(email=request.user).update(notify=True)
            return Response({'res': True, 'message': 'True', 'reason': 'update okay'}, status=status.HTTP_200_OK)


class SearchPropertyAPIView(ListAPIView):
    serializer_class = PropertySerializer
    queryset = PropertyListing.objects.all()
    filter_fields = ('city', 'address', 'state', 'amount', 'address', 'beds', 'baths')
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)

class SearchHotelAPIView(SearchPropertyAPIView):
    serializer_class = HotelSerializer
    queryset = HotelListing.objects.all()
    filter_fields = ('city', 'address', 'state', 'address')

class SearchSupplierAPIView(SearchPropertyAPIView):
    serializer_class = SupplierSerializer
    queryset = SupplierListing.objects.all()
    filter_fields = ('name', )



class ViewAllProperty(ListAPIView):
    serializer_class = PropertySerializer
    queryset = PropertyListing.objects.all()
    permission_classes = (IsAuthenticated,)

class ViewAllLand(ListAPIView):
    serializer_class = LandSerializer
    queryset = LandListing.objects.all()
    permission_classes = (IsAuthenticated,)


class ViewAllHotel(ListAPIView):
    serializer_class = Hotel
    queryset = HotelInfo.objects.all()
    permission_classes = (IsAuthenticated,)


class ViewHotelRooms(ListAPIView):
    serializer_class = HotelSerializer
    
    queryset = HotelListing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        room_id = self.request.query_params.get('id')
        return HotelListing.objects.filter(order_uuid=room_id).all()
      


class ViewPropertyAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PropertySerializer
    queryset = PropertyListing
    lookup_url_kwarg = 'id'

class ViewLandAPIView(ListAPIView):
    serializer_class = LandSerializer
    queryset = LandListing.objects.all()
    permission_classes = (IsAuthenticated,)


class ViewHotelAPIView(ListAPIView):
    serializer_class = Hotel
    queryset = HotelInfo.objects.all()
    permission_classes = (IsAuthenticated,)


class ViewServicesAPIView(ListAPIView):
    serializer_class = ServicesSerializer
    queryset = ServicesInfo.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.query_params.get('service_type', None)
        user_address = self.request.query_params.get('address', None)
        if user and user_address:
            return ServicesInfo.objects.filter(service_type=user, office_address__icontains=user_address)
        
        elif user:
            return ServicesInfo.objects.filter(service_type=user)

        elif user_address:
            return ServicesInfo.objects.filter(office_address__icontains=user_address)

        return self.queryset


class ViewServicesInfo(ListAPIView):
    serializer_class = ServicesInfoSerializer
    
    queryset = ServicesListing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        room_id = self.request.query_params.get('id')
        return ServicesListing.objects.filter(order_uuid=room_id).all()
 
   

class ViewSupplierAPIView(ListAPIView):
    queryset = SupplierListing.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)




class NearbyHotelAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = HotelInfo
    serializer_class = Hotel

    def get_queryset(self):
        lat = self.request.query_params.get('lat', None)
        lon = self.request.query_params.get('long', None)
        dis = self.request.query_params.get('dis', None)

        if lat is not None and lon is not None:
            self.request_params_validation(lat, lon)

            try:
                pnt = GEOSGeometry('POINT({} {})'.format(lon, lat))
            except GEOSException:
                pass
            else:
                if dis is  None:
                    queryset = self.queryset.objects.filter(location__dwithin=(pnt, D(km=200))).all()
                    return queryset
                else:
                    distance = int(dis)
                    queryset = self.queryset.objects.filter(location__dwithin=(pnt, D(km=distance))).all()
                    return queryset


        else:
            raise ValidityError({'res': False, 'reason': 'An error occured getting your current location',
                                 'message': 'no params'})

    def request_params_validation(self, lat, long):
        try:
            change_value_lat = float(lat)
            change_value_long = float(long)
        except ValueError:
            raise ValidityError({'res': False, 'reason': 'invalid params type', 'message': 'False'})
        else:
            if isinstance(change_value_lat, float) and isinstance(change_value_long, float):
                return True


class NearbyPropertiesAPIView(NearbyHotelAPIView):
    serializer_class = PropertySerializer
    queryset = PropertyListing

class NearbySupplierAPIView(NearbyHotelAPIView):
    serializer_class = SupplierSerializer
    queryset = SupplierListing


class NearbyProfessionalAPIView(NearbyHotelAPIView):
    serializer_class = ProfessionalSerializer
    queryset = ProfessionalListing

class NearbyServicesAPIView(NearbyHotelAPIView):
    queryset = ServicesInfo
    serializer_class = ServicesSerializer



class NearbyLandAPIView(NearbyHotelAPIView):
    queryset = LandListing
    serializer_class = LandSerializer 




class SearchPropertybyAddress(ListAPIView):
    serializer_class = PropertySerializer
    queryset = PropertyListing
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        user_address = self.request.query_params.get('address', '')
        user_beds = self.request.query_params.get('beds', 0)
        user_price = self.request.query_params.get('price', 0)
        if user_beds == 0 and user_price == 0:
            return self.queryset.objects.filter(Q(address__icontains=user_address) | 
            Q(city__icontains=user_address) | Q(state__icontains=user_address))

        elif user_price == 0:
            return self.queryset.objects.filter(Q(address__icontains=user_address, beds=user_beds) | 
            Q(city__icontains=user_address, beds=user_beds) | Q(state__icontains=user_address, beds=user_beds))

        elif user_beds == 0:
            return self.queryset.objects.filter(Q(address__icontains=user_address, amount__lte=user_price) | 
            Q(city__icontains=user_address, amount__lte=user_price) | Q(state__icontains=user_address, amount__lte=user_beds))

        else:
            return self.queryset.objects.filter(Q(address__icontains=user_address, beds=user_beds, amount__lte=user_price) | 
            Q(city__icontains=user_address, beds=user_beds, amount__lte=user_price) | Q(state__icontains=user_address, beds=user_beds, amount__lte=user_price))


class SearchLandbyAddress(SearchPropertybyAddress):
    serializer_class = LandSerializer
    queryset = LandListing


class SearchHotelbyAddress(SearchPropertybyAddress):
    serializer_class = Hotel
    queryset = HotelInfo

class SearchSupplierAddress(SearchPropertybyAddress):
    serializer_class = SupplierInfo
    queryset = Supplier

    def get_queryset(self):
        address = self.request.query_params.get('address', '')
        return self.queryset.objects.filter(office_address__icontains=address)

class  SearchServicesAddress(SearchSupplierAddress):
    serializer = ServicesSerializer
    queryset = ServicesInfo


