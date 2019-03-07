from django.contrib import admin

# Register your models here.
from .models import PropertyListing, LandListing

admin.site.register(PropertyListing)
admin.site.register(LandListing)