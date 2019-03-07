from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField

import cloudinary



class HotelListing(models.Model):
    listing_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_listing')
    hotel_name = models.CharField(max_length=250, default='')
    title = models.CharField(max_length=250)
    room_price = models.DecimalField(max_digits=20, decimal_places=2)
    room_quality = models.IntegerField(default=0)
    facilites = ArrayField(models.CharField(max_length=250))
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=250)
    website = models.URLField(blank=True)
    order_uuid = models.CharField(max_length=250)
    image_one = cloudinary.models.CloudinaryField('image')
    image_two = cloudinary.models.CloudinaryField('image')
    image_three = cloudinary.models.CloudinaryField('image')
    image_four = cloudinary.models.CloudinaryField('image')

    location = models.PointField(null=True, geography=True)
    email = models.EmailField(blank=True)
    pub_dat = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=200)
    phone_number2 = models.CharField(max_length=200, blank=True, null=True)
 

    

    def __str__(self): 
        return self.title




