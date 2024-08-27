from rest_framework import serializers
from .models import Employee, Attendance, DailyProgress

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class DailyProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProgress
        fields = ['date', 'hours_worked']

class EmployeeMonthlyReportSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_username = serializers.CharField()
    daily_progress = DailyProgressSerializer(many=True)

