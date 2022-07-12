from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

def add_zero(num):
    if num < 10:
        return '0'+str(num)
    return str(num)

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

    def rank_view(self):
        lwp_sc = self.longest_work_period
        lwp_mn = lwp_sc // 60
        lwp_sc %= 60
        lwp_hr = lwp_mn // 60
        lwp_mn %= 60
        lwp_sc = add_zero(lwp_sc)
        lwp_mn = add_zero(lwp_mn)
        lwp_hr = add_zero(lwp_hr)

        wt_sc = self.work_total
        wt_mn = wt_sc // 60
        wt_sc %= 60
        wt_hr = wt_mn // 60
        wt_mn %= 60
        wt_sc = add_zero(wt_sc)
        wt_mn = add_zero(wt_mn)
        wt_hr = add_zero(wt_hr)

        return {
            "user": self.owner.username,
            "lwp": f'{lwp_hr}:{lwp_mn}:{lwp_sc}',
            "wt": f'{wt_hr}:{wt_mn}:{wt_sc}',
            "time": self.timestamp.strftime("%b %d, %Y, %H:%M"),
        }