from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings

# Create your models here.
class GovermentListing(models.Model):
    government_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    service_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(null=True, geography=True)


    def save(self, *args, **kwargs):
        self.location = GEOSGeometry('POINT({} {})'.format(self.longitude, self.latitude))
        super().save(*args,**kwargs)

    


    def __str__(self):
        return self.description


