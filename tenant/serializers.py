from rest_framework import serializers
from django.utils import timezone
from .models import Tenant,EmergencyContacts,Guarantors,Lease,LeaseTermination,TenantDocuments


class TenantSerializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Tenant
        exclude = ['added_by']
        # list_serializer_class = BulkCreateListSerializer

    # def validate_name(self,value):
    #     print('nnnnnnnnnnnnnnnname validation')
    #     print(value)
    #     if value =="Joseph Disraeli":
    #         raise serializers.ValidationError("Blasphomey, I am a god")
    #     return value
class EmergencyContacts_serializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = EmergencyContacts
        exclude = ['added_by']
        # list_serializer_class = BulkCreateListSerializer

class Guarantors_serializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Guarantors
        exclude = ['added_by']
        # list_serializer_class = BulkCreateListSerializer
class Lease_serializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Lease
        exclude = ['added_by']
        # list_serializer_class = BulkCreateListSerializer


class Terminate_serializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = LeaseTermination
        exclude = ['added_by']

class Document_serializer(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = TenantDocuments
        exclude = ['added_by']
