from rest_framework import serializers
from .models import Maintenance,Cost,Document
from django.utils import timezone



class MaintenanceSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))

    class Meta:
        model = Maintenance
        exclude = ['added_by']

class CostSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Cost
        exclude = ['added_by']
class DocumentSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Document
        exclude = ['added_by']