from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Employee, Attendance, DailyProgress
from .serializers import EmployeeMonthlyReportSerializer, EmployeeSerializer, AttendanceSerializer, DailyProgressSerializer
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status

class EmployeeListCreate(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceListCreate(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class DailyProgressListCreate(generics.ListCreateAPIView):
    queryset = DailyProgress.objects.all()
    serializer_class = DailyProgressSerializer

class CheckInView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, card_id):
        try:
            employee = Employee.objects.get(card_id=card_id)
            check_in_time = timezone.now()
            attendance = Attendance.objects.create(employee=employee, check_in=check_in_time)
            
            # Update daily progress
            today = check_in_time.date()
            daily_progress, created = DailyProgress.objects.get_or_create(employee=employee, date=today)
            daily_progress.save()
            
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

class CheckOutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, card_id):
        try:
            employee = Employee.objects.get(card_id=card_id)
            check_out_time = timezone.now()
            attendance = Attendance.objects.filter(employee=employee, check_out__isnull=True).latest('check_in')
            attendance.check_out = check_out_time
            attendance.save()
            
            # Update daily progress
            today = check_out_time.date()
            total_hours = sum([(attendance.check_out - attendance.check_in).total_seconds() / 3600 for attendance in Attendance.objects.filter(employee=employee, check_in__date=today) if attendance.check_out])
            daily_progress, created = DailyProgress.objects.get_or_create(employee=employee, date=today)
            daily_progress.hours_worked = total_hours
            daily_progress.save()
            
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Attendance.DoesNotExist:
            return Response({"error": "No active check-in found for this employee"}, status=status.HTTP_400_BAD_REQUEST)


class MonthlyReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, year, month):
        try:
            start_date = timezone.datetime(year, month, 1)
            end_date = (start_date + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(seconds=1)
            
            # Fetch all employees
            employees = Employee.objects.all()
            report_data = []

            for employee in employees:
                daily_progress = DailyProgress.objects.filter(employee=employee, date__range=(start_date, end_date)).order_by('date')
                employee_data = {
                    'employee_id': employee.id,
                    'employee_username': employee.user.username,
                    'daily_progress': DailyProgressSerializer(daily_progress, many=True).data
                }
                report_data.append(employee_data)

            serializer = EmployeeMonthlyReportSerializer(report_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



