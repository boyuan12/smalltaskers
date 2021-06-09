from django.db import models
from django.conf import settings

# Create your models here.
class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    start_date = models.DateField(auto_now=True)
