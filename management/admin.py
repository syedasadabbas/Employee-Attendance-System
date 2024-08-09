from django.contrib import admin
from .models import Employee, Attendance, DailyProgress
# Register your models here.
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(DailyProgress)