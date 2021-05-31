from django.db import models
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    member_username = models.CharField(max_length=30)
