import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduled_email_system.settings')

app = Celery('scheduled_email_system')

# Load settings from Django settings.py (CELERY_*)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in all installed apps
app.autodiscover_tasks()