"""real_estate_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('property/', include('real_estate_api.owner.urls')),
    path('hotel/', include('real_estate_api.hotel.urls')),
    path('customer/', include('real_estate_api.customer.urls')),
    path('owner/', include('real_estate_api.owner.urls')),
    path('supplier/', include('real_estate_api.supplier.urls')),
    path('professional/', include('real_estate_api.professional.urls')),
    path('government/', include('real_estate_api.government.urls')),
    path('valuer/', include('real_estate_api.valuer.urls')),
    path('developer/', include('real_estate_api.developer.urls')),
    path('services/', include('real_estate_api.services.urls')),
    path('blog/', include('real_estate_api.blog.urls')),
    path('notification/', include('real_estate_api.notification.urls')),
    path('messenger/', include('real_estate_api.messager.urls')), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
