from django.urls import path
from  . import views

urlpatterns = [
    path('create-post/', views.CreateHotelPost.as_view(), name='create'),
    path('edit-institute/<int:pk>/', views.RetrieveHotelPost.as_view(), name='retrieve'),
    path('view-institute/', views.ListHotelPost.as_view(), name='list'),
    path('delete-institute/<int:pk>/', views.DeleteHotelPost.as_view(), name='delete')
]