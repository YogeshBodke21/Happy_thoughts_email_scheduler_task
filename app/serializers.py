from rest_framework import serializers
from .models import ScheduleEmail

class ScheduleEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEmail
        fields = '__all__'
        read_only_fields = ['status']

        