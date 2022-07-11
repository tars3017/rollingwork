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
        return f'({self.id}) {self.owner.username} at {self.timestamp.strftime("%b %d, %Y, %H:%M")}'

    def brief_view(self):
        efficiency = int(self.work_total / self.app_total * 100)
        return {"history_str": f'{self.timestamp.strftime("%b %d, %Y, %H:%M")} Total: {int(self.app_total/3600)}hr Efficiency: {efficiency}%',
                "id": self.id
        }