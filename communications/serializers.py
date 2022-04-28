from rest_framework import serializers
from .models import Email
from django.utils import timezone



class EmailSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Email
        exclude = ['added_by']
