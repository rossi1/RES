from django.contrib.gis.db import models
from django.conf import settings

import cloudinary


#from notification.models import Notification


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog')
    title = models.CharField(max_length=250)
    posted = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users', null=True)
    has_seen = models.BooleanField(default=False)
    image = cloudinary.models.CloudinaryField('image')

    def __str__(self):
        return str(self.title)

    '''
    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)
        i_d = Blog.objects.get(pk=self.pk)
        Notification.objects.create(blog=i_d)
    '''   



