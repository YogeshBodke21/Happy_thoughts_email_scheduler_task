from django.db import models

# Create your models here.

class ScheduleEmail(models.Model):
    status_choices = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    )

    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_to = models.EmailField()
    sent_at = models.DateTimeField()
    status = models.CharField(choices=status_choices, default='pending')
    task_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.subject} --> {self.sent_to}"


