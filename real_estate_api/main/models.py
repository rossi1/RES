from django.db import models 
from django.conf import settings

class Services(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=250)
    service_type = models.CharField(max_length=250)