
from .base import *


from decouple import config

DEBUG=True


DATABASES = {
   'default': {
       'ENGINE':'django.contrib.gis.db.backends.postgis',
       'NAME': config('DB_NAME'),
       'USER': config('DB_USER'),
       'PASSWORD': config('DB_PASSWORD'),
       'HOST': '127.0.0.1',
       'PORT': ''
   }
    

}




