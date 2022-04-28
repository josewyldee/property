from rest_framework import serializers
from django.utils import timezone
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Notification
        exclude = ['date']
