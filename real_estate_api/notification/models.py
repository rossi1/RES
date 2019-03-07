from django.conf import settings
from django.contrib.gis.db import models



'''
class Notification(models.Model):
    blog = models.ForeignKey('blog.Blog', on_delete=models.CASCADE, related_name='notify_blog')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users', null=True)
    has_seen = models.BooleanField(default=False)


    def __str__(self):
        return str(self.blog)

'''