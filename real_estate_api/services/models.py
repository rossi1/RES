from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

import cloudinary

# Create your models here.
class ServicesListing(models.Model):
    services_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    topic = models.CharField(max_length=250)
    image = cloudinary.models.CloudinaryField('image')
    pub_date = models.DateTimeField(auto_now_add=True)
    location = models.PointField(null=True, geography=True)
    order_uuid = models.CharField(max_length=250, default='')
   
    



 
    def __str__(self):
        return self.description


