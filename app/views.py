from django.shortcuts import render
from .models import ScheduleEmail
from .serializers import ScheduleEmailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import pytz
from .tasks import send_schedule_email
# Create your views here.

IST = pytz.timezone('Asia/Kolkata')

class ScheduleMailView(APIView):
    def post(self, request):
        print(request.data)
        serializer = ScheduleEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.save(status='pending')
            send_schedule_email.apply_async(args=[email.id], eta = email.sent_at)

            #convet UTC to IST for user
            scheduled_ist = email.sent_at.astimezone(IST).strftime("%d-%m-%Y %I:%M %p")
            return Response({
                "message":"Email sent successfully!",
                "email":email.sent_to,
                "sent_at":scheduled_ist

            }, status=status.HTTP_200_OK)
        return Response({
            "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


'''
sample body for post request:--
{
  "sent_to": "ybodke123@gmail.com",
  "subject": "Hello from Django",
  "message": "This is a test scheduled email.",
  "sent_at": "2026-03-27T13:30:00+05:30"
}'''