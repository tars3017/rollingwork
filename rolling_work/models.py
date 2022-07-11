from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Record(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # app data (counted by seconds)
    longest_work_period = models.IntegerField(default=0)
    shortest_work_period = models.IntegerField(default=0)
    longest_rest_period = models.IntegerField(default=0)
    shortest_rest_period = models.IntegerField(default=0)
    work_total = models.IntegerField(default=0)
    app_total = models.IntegerField(default=0)
    roll_count = models.IntegerField(default=0)

    def __str__(self):
        return f'({self.id}) {self.owner.username} at {self.timestamp.strftime("%b %d %Y, %H:%M")}'