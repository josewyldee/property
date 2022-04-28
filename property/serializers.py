from rest_framework import serializers
from .models import Property,Unit,Unit_photos,Unit_features,Property_documents, Utility_bills
from django.utils import timezone



class PropertySerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Property
        exclude = ['added_by']
class UnitSerializers(serializers.ModelSerializer):
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Unit
        # fields = ['id','unit_name','unit_property','added_on']
        exclude = ['added_by','last_updated']
        # exclude = ['added_by','last_updated','create_nos','unit_charges']
class FeaturesSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Unit_features
        exclude = ['added_by']
class PhotoSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Unit_photos
        exclude = ['added_by']
class DocumentSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Property_documents
        exclude = ['added_by']
class UtilitySerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Utility_bills
        exclude = ['added_by']



