from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, date
from .models import Attendance, User
import json

# JSON response
# @csrf_exempt
# def mark_in_time(request, uid):
#     if request.method == 'POST':
#         in_time = timezone.now()
#         attendance, created = Attendance.objects.get_or_create(
#             employee_id=uid,
#             date=date.today(),
#             defaults={'in_time': in_time}
#         )
#         if not created:
#             attendance.in_time = in_time
#             attendance.save()
#         return JsonResponse({'status': 'Check-in time marked', 'in_time': in_time})

# Templates Rendering
@csrf_exempt
def mark_in_time(request, uid):
    if request.method == 'POST':
        in_time = timezone.now()
        attendance, created = Attendance.objects.get_or_create(
            user_id=uid,
            date=date.today(),
            defaults={'in_time': in_time}
        )
        if not created:
            attendance.in_time = in_time
            attendance.save()
        context = {
            'uid': uid,
            'status': 'Check-in time marked',
            'in_time': in_time,
        }
        return render(request, 'checkin.html', context)
    else:
        return render(request, 'checkin.html', {'uid': uid})

# JSON response
# @csrf_exempt
# def mark_out_time(request, uid):
#     if request.method == 'POST':
#         try:
#             attendance = Attendance.objects.get(employee_id=uid, date=date.today(), out_time__isnull=True)
#             attendance.out_time = timezone.now()
#             attendance.save()
#             return JsonResponse({
#                 'status': 'Check-out time marked',
#                 'out_time': attendance.out_time,
#                 'total_hours': attendance.total_time_hours
#             })
#         except Attendance.DoesNotExist:
#             return JsonResponse({'status': 'Error', 'message': 'No check-in found for today for this user'})

# Templates Rendering
@csrf_exempt
def mark_out_time(request, uid):
    if request.method == 'POST':
        try:
            attendance = Attendance.objects.get(employee_id=uid, date=date.today(), out_time__isnull=True)
            attendance.out_time = timezone.now()
            attendance.save()
            context = {
                'uid': uid,
                'status': 'Check-out time marked',
                'out_time': attendance.out_time,
                'total_hours': attendance.total_time_hours,
            }
            return render(request, 'checkout.html', context) 
        except Attendance.DoesNotExist:
            context = {
                'uid': uid,
                'status': 'Error: No check-in found for today for this user'
            }
            return render(request, 'checkout.html', context)  
    else:
        return render(request, 'checkout.html', {'uid': uid})

# JSON Response
# def get_attendance_details(request, uid):
#     try:
#         attendance = Attendance.objects.get(employee_id=uid)
#         return JsonResponse({
#             'employee_id': attendance.employee_id,
#             'in_time': attendance.in_time,
#             'out_time': attendance.out_time,
#             'total_hours': attendance.total_time_hours
#         })
#     except Attendance.DoesNotExist:
#         return JsonResponse({'status': 'Error', 'message': 'No attendance record found for this user'})

# Templates Rendering
def get_attendance_details(request, uid):
    try:
        attendance = Attendance.objects.get(employee_id=uid, date=date.today())  
        context = {
            'employee_id': attendance.employee_id,
            'in_time': attendance.in_time,
            'out_time': attendance.out_time,
            'total_hours': attendance.total_time_hours,
        }
        return render(request, 'attendance_details.html', context)
    except Attendance.DoesNotExist:
        context = {
            'status': 'Error: No attendance record found for this user',
            'uid': uid
        }
        return render(request, 'attendance_details.html', context) 

# JSON Rensponse
# def mark_absent(uid):
#     Attendance.objects.get_or_create(
#         employee_id=uid,
#         date=date.today(),
#         defaults={'total_time_hours': 0.0}
#     )

# Templates Rendering
@csrf_exempt
def mark_absent(request, uid):
    if request.method == 'POST':
        Attendance.objects.get_or_create(
            employee_id=uid,
            date=date.today(),
            defaults={'total_time_hours': 0.0}
        )
        context = {
            'uid': uid,
            'status': 'Absent marked for today with 0 hours'
        }
        return render(request, 'mark_absent.html', context)
    else:
        return render(request, 'mark_absent.html', {'uid': uid})

def status_view(request):
    context = {
        'uid': request.user.id, 
        'status': 'Successfully checked in!'
    }
    return render(request, 'checkin.html', context)
