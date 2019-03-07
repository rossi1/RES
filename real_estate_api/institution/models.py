from django.contrib.gis.db import models
from django.conf import settings

# Create your models here.
class InstituteListing(models.Model):
    institute_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    service_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    pub_date = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.description


