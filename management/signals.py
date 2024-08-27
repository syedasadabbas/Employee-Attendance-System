# management/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Attendance, DailyProgress

@receiver(post_save, sender=Attendance)
def update_daily_progress(sender, instance, **kwargs):
    if instance.check_out:
        employee = instance.employee
        today = instance.check_out.date()
        attendances = Attendance.objects.filter(employee=employee, check_in__date=today)
        total_hours = sum([(attendance.check_out - attendance.check_in).total_seconds() / 3600 for attendance in attendances if attendance.check_out])
        daily_progress, created = DailyProgress.objects.get_or_create(employee=employee, date=today)
        daily_progress.hours_worked = total_hours
        daily_progress.save()
