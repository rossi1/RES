from collections import OrderedDict 

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .serializer import UserPortFolioSerializer


from accounts.models import Estate
from accounts.authentication import JwtAuthentication

class UpdateUserPortFolio(RetrieveUpdateAPIView):
    authentication_classes = (SessionAuthentication, JwtAuthentication)
    serializer_class = UserPortFolioSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Estate
    lookup_field = 'pk'



class CreateEstate(CreateAPIView):
    authentication_classes = (SessionAuthentication, JwtAuthentication)
    serializer_class = UserPortFolioSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Estate
    
    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'reason': 'created successfully', 'res': True, 'message': 'True'}, status=status.HTTP_200_OK)
        else:
            return Response({'reason': serializer.errors, 'res': False, 'message': 'False'}, status=status.HTTP_200_OK)

    

class ListEstate(ListAPIView):
    authentication_classes = (SessionAuthentication, JwtAuthentication)
    serializer_class = UserPortFolioSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Estate


    def get_queryset(self):
        return self.queryset.objects.filter(user=self.request.user)



@api_view(['POST'])
def create_portfolio(request):
    try:
        instance = Estate.objects.get(user=request.user)
    except Estate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = UserPortFolioSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'res': True, 'message': 'True'}, status=status.HTTP_200_OK)
            


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def  view_profile(request):
    data =  OrderedDict()

    if request.user.is_property_owner:
       
        data['user'] = {
            'account_type': 'property owner',
            'full_name': request.user.owner.full_name,
            'contact_address': request.user.owner.contact_address,
            'gender': request.user.owner.gender,
            'profile_picture': request.user.owner.profile_picture.url,
            'user': {'email': request.user.email, 'contact_number': request.user.contact_number
            }


        }
         
    elif request.user.is_customer:
        
        data['user'] = {
            'account_type': 'customer',
            'full_name': request.user.customer.full_name,
            'contact_address': request.user.customer.contact_address,
            'profile_picture': request.user.customer.profile_picture.url,
            'user_data': {'email': request.user.email, 'contact_number': request.user.contact_number
            }


        }

    elif request.user.is_developer or request.user.is_government or request.user.is_valuer or request.user.is_supplier or request.user.is_agent:
           data['user'] = {
            'account_type': request.user.developer.service_type,
            'full_name': request.user.developer.full_name,
            'contact_address': request.user.developer.office_address,
            'profile_picture': request.user.developer.profile_picture.url,
            'user_data': {'email': request.user.email, 'contact_number': request.user.contact_number
            }

        }
      
     
    elif request.user.is_hotelier:
        data['user'] = {
            'account_type': 'hotelier',
            'full_name': request.user.hotelier.hotel_name,
            'contact_address': request.user.hotelier.address,
            'profile_picture': request.user.hotelier.profile_picture.url,
            'user_data': {'email': request.user.email, 'contact_number': request.user.contact_number
            }

        }

    elif request.user.is_institute:
            data['user'] = {
            'account_type':'institute',
            'full_name': request.user.institute.institute_name,
            'contact_address': request.user.institute.institute_address,
            'profile_picture': request.user.institute.profile_picture.url,
            'user_data': {'email': request.user.email, 'contact_number': request.user.contact_number
            }

        }

       

    return Response({'data': data,
    'message': 'true', 'reason': 'true'})