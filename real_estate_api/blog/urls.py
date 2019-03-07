from django.urls import path

from . import views

urlpatterns = [
    path('view-blog/', views.ListBlog.as_view(), name='blog')
]