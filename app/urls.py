from django.urls import path
from .views import ScheduleMailView, reschedule_email

urlpatterns = [
    path("schedule_task/", ScheduleMailView.as_view()),
    path("reschedule_task/<int:pk>", reschedule_email)
]