from django.urls import path
from .views import EmployeeListCreate, AttendanceListCreate, DailyProgressListCreate, CalculateDailyProgress, CheckInView, CheckOutView, MonthlyReportView

urlpatterns = [
    path('employees', EmployeeListCreate.as_view(), name='employee-list-create'),
    path('attendances', AttendanceListCreate.as_view(), name='attendance-list-create'),
    path('daily-progress/', DailyProgressListCreate.as_view(), name='daily-progress-list-create'),
    path('calculate-daily-progress/<str:card_id>', CalculateDailyProgress.as_view(), name='calculate-daily-progress'),
    path('check-in/<str:card_id>', CheckInView.as_view(), name='check-in'),
    path('check-out/<str:card_id>', CheckOutView.as_view(), name='check-out'),
    path('monthly-report/<int:year>/<int:month>', MonthlyReportView.as_view(), name='monthly-report'),
]
