from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Estate, HotelInfo, Supplier, Customer, AgentInfo, PropertyOwnerInfo, ServicesInfo
# Register your models here.

admin.site.register(get_user_model())

admin.site.register(Estate)
admin.site.register(HotelInfo)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(AgentInfo)
admin.site.register(PropertyOwnerInfo)
admin.site.register(ServicesInfo)