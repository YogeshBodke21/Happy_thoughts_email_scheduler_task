from django.urls import path
from .views import ScheduleMailView

urlpatterns = [
    path("schedule_task/", ScheduleMailView.as_view())
]