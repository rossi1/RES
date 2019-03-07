from django.urls import path

from . import views

urlpatterns = [
    path('create-property-listing/', views.PropertyListingCreateAPIView.as_view()),
    path('create-land-listing/', views.LandListingCreateAPIView.as_view()),
    path('view-property/', views.ListPropertyAPIView.as_view()),
    path('view-land/', views.ListLandAPIView.as_view()),
    path('update-property/<int:pk>/', views.UpdatePropertyAPIView.as_view()),
    path('update-land/int:pk>/', views.UpdateLandAPIView.as_view()),
    path('delete-property/<int:pk>/', views.DeletePropertyAPIView.as_view()),
    path('delete-land/<int:pk>/', views.DeleteLandAPIView.as_view())
]

