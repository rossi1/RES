
from .base import *

import dj_database_url
from decouple import config



DATABASES = {}

DATABASES['default'] =  dj_database_url.config(default=config('DATABASE_URL'))
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

"""

GEOS_LIBRARY_PATH = "{}/libgeos_c.so".format(os.environ.get('GEOS_LIBRARY_PATH'))
GDAL_LIBRARY_PATH = "{}/libgdal.so".format(os.environ.get('GDAL_LIBRARY_PATH'))
PROJ4_LIBRARY_PATH = "{}/libproj.so".format(os.environ.get('PROJ4_LIBRARY_PATH'))

"""
GDAL_LIBRARY_PATH = "/app/.heroku/vendor/lib/libgdal.so"
GEOS_LIBRARY_PATH = "/app/.heroku/vendor/lib/libgeos_c.so"
