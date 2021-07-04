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

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    proof = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default="pending") # approved, revise, pending