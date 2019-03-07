from django.urls import path

from . import views

urlpatterns = [
    path('view-profile/', views.view_profile, name='view_profile'),
    path('estate-create/', views.CreateEstate.as_view(), name='create-estate'),
    path('estate-view/', views.ListEstate.as_view(), name='list_estate'),
    path('update-estate/<int:pk>/', views.UpdateUserPortFolio.as_view(), name='update-portfolio')
]