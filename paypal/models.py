from django.db import models
from django.conf import settings


# Create your models here.
class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    status = models.CharField(max_length=10) # deposit, withdraw
    amount = models.FloatField()


class UserFund(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    fund = models.FloatField()
