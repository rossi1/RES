from django.urls import path

from . import views

urlpatterns = [
    path('update-notification/', views.NotificationAPIView.as_view(), name='notify'),
    path('view-properties/', views.ViewAllProperty.as_view(), name='view_property'),
    path('view-land/', views.ViewAllLand.as_view(), name='view_land'),
    path('view-services/', views.ViewServicesAPIView.as_view(), name='services'),
    
    path('view-supplier/', views.ViewSupplierAPIView.as_view(), name='view_supplier'),

    path('search-property/', views.SearchPropertyAPIView.as_view(), name='search'),
    path('search-hotel/', views.SearchHotelAPIView.as_view(), name='search'),
    path('search-supplier/', views.SearchSupplierAPIView.as_view(), name='search'),
    #path('agents/', views.ListPropertyAgentAPIView.as_view(), name='agents'),
    path('property/<str:id>/', views.ViewPropertyAPIView.as_view(), name='view'),
    path('nearby-hotel/', views.NearbyHotelAPIView.as_view(), name='nearby hotel'),
    path('view-service-works/', views.ViewServicesInfo.as_view(), name='service_info' ),

    
    
    path('nearby-services/', views.NearbyServicesAPIView.as_view(), name='nearby services'),
    path('nearby-supplier/', views.NearbySupplierAPIView.as_view(), name='nearby supplier'),
    path('nearby-land/', views.NearbyLandAPIView.as_view(), name='nearby land'),
    path('view-hotel/', views.ViewAllHotel.as_view(), name='hotel'),
    path('view-hotel-rooms/', views.ViewHotelRooms.as_view(), name='hotel rooms'),
    path('nearby-property/', views.NearbyPropertiesAPIView.as_view(), name='nearby property'),
    path('nearby-professional/', views.NearbyProfessionalAPIView.as_view(), name='nearby professional'),
    path('search-property-address/', views.SearchPropertybyAddress.as_view(), name='property'),
    path('search-land-address/', views.SearchLandbyAddress.as_view(), name='land'),
    path('search-hotel-address/', views.SearchHotelbyAddress.as_view(), name='hotel'),
    path('search-supplier-address/', views.SearchSupplierAddress.as_view(), name='supplier'),
    path('search-service-address/', views.SearchServicesAddress.as_view(), name='service')
    
    
]