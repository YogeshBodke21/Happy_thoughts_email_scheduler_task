from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import ScheduleEmail

@shared_task
def send_schedule_email(id):
    try:
        obj = ScheduleEmail.objects.get(id = id)
        if obj.status != 'pending':
            return f"Email has already sent to {obj.sent_to}!!"
        
        send_mail(
            subject=obj.subject,
            message=obj.message,
            from_email=settings.DEFAULT_FROM_EMAIL,  
            recipient_list=[obj.sent_to],             # must be a list or tuple
            fail_silently=False
        )

        obj.status = 'sent'
        obj.save()
        print("sent to user!!")
    except Exception as e:
        obj.status = 'failed'
        obj.save()
        return str(e)

