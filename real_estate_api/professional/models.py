from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings


class ProfessionalListing(models.Model):
    listing_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    brand_type = models.CharField(max_length=250)
    brand_address = models.CharField(max_length=250)
    services_offered = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.CharField(max_length=250)
    services_charge = models.DecimalField(decimal_places=10, max_digits=19)
    location = models.PointField(null=True, geography=True)

    def save(self, *args, **kwargs):
        self.location = GEOSGeometry('POINT({} {})'.format(self.longitude, self.latitude))
        super().save(*args,**kwargs)

    def __str__(self):
        return str(self.listing_id)