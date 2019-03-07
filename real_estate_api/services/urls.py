from django.urls import path
from  . import views

urlpatterns = [
    path('create-post/', views.CreateHotelPost.as_view(), name='create'),
    path('edit-service/<int:pk>/', views.RetrieveHotelPost.as_view(), name='retrieve'),
    path('view-service/', views.ListHotelPost.as_view(), name='list'),
    path('delete-service/<int:pk>/', views.DeleteHotelPost.as_view(), name='delete')
]