from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

import cloudinary


class PropertyListing(models.Model):
    CHOICE = (
        ('residential','residential'),
        ('commercial', 'commercial'),

        
    )

    PROPERTY_LISTING_TYPE = (
        ('condo', 'condo'),
        ('apartment', 'apartment'),
        ('home', 'home')
    )

    POSTED_BY = (
        ('property owner', 'property owner'),
        ('agent', 'agent'),
        ('tenant', 'tenant')
    )
  
    listing_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    address = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    listings = ArrayField(models.CharField(max_length=250))
    property_type = models.CharField(max_length=250)
    property_listing_type = models.CharField(max_length=250)
    prop_stats = models.BooleanField(default=False)
    beds = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    photo_one = cloudinary.models.CloudinaryField('image')
    photo_two = cloudinary.models.CloudinaryField('image')
    photo_three = cloudinary.models.CloudinaryField('image')
    photo_four = cloudinary.models.CloudinaryField('image')
    photo_five = cloudinary.models.CloudinaryField('image')
    square_feet = models.FloatField(default=137.26)
    contact_profile_photo = cloudinary.models.CloudinaryField('image')
    contact_number = models.CharField(max_length=250, blank=True)
    contact_name = models.CharField(max_length=250, blank=True)
    contact_email = models.EmailField(blank=True)
    posted_by = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(null=True, geography=True)
    videolink = ArrayField(models.URLField(blank=True), blank=True)

    def save(self, *args, **kwargs):
        self.location = GEOSGeometry('POINT({} {})'.format(self.longitude, self.latitude))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.listing_id)


class LandListing(models.Model):
    POSTED_BY = (
        ('property owner', 'property owner'),
        ('agent', 'agent'),
        ('tenant', 'tenant')
        )

    listing_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField(max_length=250)
    land_photo = cloudinary.models.CloudinaryField('image')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    mortgages = models.BooleanField(default=False)
    taxes = models.BooleanField(default=False)
    owner_association = models.BooleanField(default=False)
    state = models.CharField(max_length=250)
    water_source  = models.CharField(max_length=250)
    sewer_source =  models.CharField(max_length=250)
    improvments =  models.CharField(max_length=250)
    electricity =  models.CharField(max_length=250)
    contact_profile_photo = cloudinary.models.CloudinaryField('image')
    contact_name = models.CharField(max_length=250, blank=True)
    contact_number = models.CharField(max_length=250, blank=True)
    contact_email = models.EmailField(blank=True)
    features = ArrayField(models.CharField(max_length=250))
    posted_by = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(null=True, geography=True)
    videolink = ArrayField(models.URLField(blank=True))
    photo_one = cloudinary.models.CloudinaryField('image')
    photo_two = cloudinary.models.CloudinaryField('image')
    photo_three = cloudinary.models.CloudinaryField('image')
    photo_four = cloudinary.models.CloudinaryField('image')
    photo_five = cloudinary.models.CloudinaryField('image')
    square_feet = models.FloatField(default=137.26)




    def save(self, *args, **kwargs):
        self.location = GEOSGeometry('POINT({} {})'.format(self.longitude, self.latitude))
        super().save(*args, **kwargs)
    

    def __str__(self):
        return str(self.listing_id)


    

