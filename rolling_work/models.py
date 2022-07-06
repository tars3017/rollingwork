from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Record(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    
    # app data (unit by seconds)
    longest_work_period = models.IntegerField(default=0)
    shortest_work_period = models.IntegerField(default=0)
    longest_rest_period = models.IntegerField(default=0)
    shortest_rest_period = models.IntegerField(default=0)
    work_total = models.IntegerField(default=0)
    app_total = models.IntegerField(default=0)
    roll_count = models.IntegerField(default=0)