from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

class SupplierListing(models.Model):
    listing_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    sn_measure = models.CharField(max_length=250)
    description = models.TextField()

    location = models.PointField(null=True, geography=True)

    

    def __str__(self):
        return self.name

    