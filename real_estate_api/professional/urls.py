from django.urls import path

from . import views

urlpatterns = [
    path('create-services/', views.ProfessionalCreateAPIVIew.as_view()),
    path('list-services/', views.ListProfessionalServiceAPIView.as_view()),
    path('update-service/<int:pk>/', views.UpdateProfessionalServiceAPIView.as_view()),
    path('delete-service/<int:pk>/', views.DeleteProfessionalAPIView.as_view())
]