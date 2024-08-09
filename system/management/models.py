from django.db import models
from django.utils import timezone
from datetime import timedelta, date

class User(models.Model):
    serial_number = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.serial_number} - {self.username}"
    
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    date = models.DateField(default=date.today)
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    total_time_hours = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.in_time and self.out_time:
            time_diff = self.out_time - self.in_time
            self.total_time_hours = time_diff.total_seconds() / 3600
        else:
            self.total_time_hours = 0.0
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.serial_number} - {self.date} - {self.in_time} to {self.out_time}"
