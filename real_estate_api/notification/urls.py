from django.urls import path


from . import views

urlpatterns =  [
    path('view/', views.list_notification, name='view'),
    path('read/<str:blog_id>/', views.read_blog, name='blog'),
    path('view-all/', views.list_all_notification, name='list_all')
    
]