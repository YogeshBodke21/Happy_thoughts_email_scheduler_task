from django.shortcuts import render
from .models import ScheduleEmail
from .serializers import ScheduleEmailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import pytz
from .tasks import send_schedule_email
from rest_framework.decorators import api_view
from scheduled_email_system.celery import app 
from django.utils.dateparse import parse_datetime
# Create your views here.

IST = pytz.timezone('Asia/Kolkata')

class ScheduleMailView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ScheduleEmailSerializer(data=request.data)
        if serializer.is_valid():
            email_obj = serializer.save(status='pending')
            print(email_obj.id)
            task = send_schedule_email.apply_async(args=[email_obj.id], eta = email_obj.sent_at)
            email_obj.task_id = task.id
            email_obj.save()
            #convet UTC to IST for user
            scheduled_ist = email_obj.sent_at.astimezone(IST).strftime("%d-%m-%Y %I:%M %p")
            return Response({
                "task_id" : email_obj.id, 
                "sending to":email_obj.sent_to,
                "Scheduled at":scheduled_ist,
                "status": email_obj.status

            }, status=status.HTTP_200_OK)
        return Response({
            "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def reschedule_email(request, pk):
    try:
        try:
            email_obj = ScheduleEmail.objects.get(pk=pk)
        except ScheduleEmail.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)

        new_sent_time = request.data.get("sent_at")

        if not new_sent_time:
            return Response({"error": "sent_at is required"}, status=400)

        new_sent_time = parse_datetime(new_sent_time)
        if not new_sent_time:
            return Response({"error": "Invalid datetime format"}, status=400)

        if email_obj.task_id:
            app.control.revoke(email_obj.task_id, terminate=True)

        #schedule new task
        task = send_schedule_email.apply_async(
            args=[email_obj.id],
            eta=new_sent_time
        )

        email_obj.sent_at = new_sent_time
        email_obj.status = 'pending'
        email_obj.task_id = task.id   
        email_obj.save()
        print("new sent time:--", str(email_obj.sent_at))
        # convert UTC to IST
        scheduled_ist = email_obj.sent_at.astimezone(IST).strftime("%d-%m-%Y %I:%M %p")

        return Response({
                "task_id" : email_obj.id, 
                "sending to":email_obj.sent_to,
                "Scheduled at":scheduled_ist,
                "status": email_obj.status
            }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "error": str(e),
        }, status=400)





'''
sample body for post request:--
{
  "sent_to": "ybodke123@gmail.com",
  "subject": "Hello from Django",
  "message": "This is a test scheduled email.",
  "sent_at": "2026-03-27T13:30:00+05:30"
}'''

# 27-03-2026 01:30 PM


#reschedule_task/id
# {
#   "sent_at": "2026-03-27T13:30:00+05:30"
# }


#celery cmd
#celery -A scheduled_email_system  worker --pool=solo -l info