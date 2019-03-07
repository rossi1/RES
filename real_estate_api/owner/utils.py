from django.conf import settings
from accounts.validators import ValidityError
import geocoder


def get_latlng(address):
    latlng = geocoder.google(location=address, key=settings.GOOGLE_API_KEY)
    if latlng:
        return  latlng
    else:
        raise ValidityError({'message': 'an error occured', 'res': False, 'reason': 
        'An error occured please verify your address'})


