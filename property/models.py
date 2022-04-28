
from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.conf import settings
from .managers import PropertyManager,UnitManager
from django.urls import reverse

# from staff.models import Staff
# from django.contrib.auth.models import User


User=settings.AUTH_USER_MODEL
# User=settings.AUTH_USER_MODEL
class Property(models.Model):
    class NormalData(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(active=True)
    class NormalTable(models.Manager):
        def get_queryset(self):
            return super().get_queryset().only('property_name','property_category','property_type','managed_by','owned_by','bulk','bulk_name','bulk_id').filter(active=True)
 
    property_name = models.CharField(max_length=35)
    property_category = models.CharField(max_length=35,default="Residential")
    property_type = models.CharField(max_length=35,default="Apartment buildings")
    random_value=models.CharField(max_length=50, null=True,blank=True)
    year_created=models.IntegerField(blank=True, null=True)
    property_authority = models.CharField(max_length=55)
    occupancy_status = models.CharField(
    max_length=20, blank=True, null=True, default="vacant")

    
    property_rent_name = models.CharField(max_length=35,blank=True, null=True)
    property_rent_category = models.CharField(max_length=35,default="custom")
    property_rent_amount =models.IntegerField(default=0)
    property_rent_date = models.IntegerField(blank=True, null=True)
    property_rent_duration = models.CharField(max_length=35,blank=True, null=True)

    property_owner = models.CharField(max_length=55, null=True,blank=True)
    property_use = models.CharField(max_length=55,default="rent")
    ownership_document=models.FileField(upload_to='property')
    # rent = models.ForeignKey(Charges, on_delete=models.SET_NULL,null=True,blank=True)
    
    # unit_charges=ArrayField(models.IntegerField(), blank=True,default=list)
    # tags = ArrayField(models.CharField(max_length=200), blank=True)
    country=models.CharField(max_length=50,default="Kenya")
    country_code=models.CharField(max_length=50,blank=True, null=True)
    city=models.CharField(max_length=50,default="Nairobi")
    street=models.CharField(max_length=50, null=True,blank=True)
    landmark_description=models.TextField(blank=True, null=True,max_length=350)
    # property_documents=ArrayField(models.IntegerField(), blank=True,null=True,default=list)
    # utility_bills=ArrayField(models.IntegerField(), blank=True,null=True,default=list)
    managed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='property_manager')
    owned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='property_owner')
    
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='property_added_by',null=True)
    
    active=models.BooleanField(default=True)
    photo=models.ImageField(upload_to='property',default="property/building.jpg")
    description=models.TextField(null=True,blank=True)

    objects=PropertyManager()
    @property
    def get_last_bulk_id(self):
        return Property.objects.last()
    
    def get_absolute_url(self):
        return reverse("property:details", args=[self.id])

    def __str__(self):
        return f"{self.property_name}, {self.property_type} "


    class Meta:
         verbose_name_plural = "Buildings"
         ordering = ['added_on']
       
class Unit(models.Model):
    unit_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=35)
    unit_category = models.CharField(max_length=35,default="Residential")
    unit_type = models.CharField(max_length=35,blank=True, null=True)

    size = models.IntegerField(null=True,blank=True)
    baths = models.CharField(max_length=10, blank=True, null=True)
    is_furnished = models.CharField(max_length=5,default="yes")
    water_mtr = models.CharField(max_length=45, blank=True, null=True)
    electricity_mtr = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    bedrooms=models.IntegerField(default=1)
    
    # tags = ArrayField(models.CharField(max_length=200), blank=True,null=True)
    unit_charges = ArrayField(models.CharField(max_length=200), blank=True,null=True)
    unit_features = ArrayField(models.CharField(max_length=200), blank=True,null=True)
    unit_photos = ArrayField(models.CharField(max_length=200), blank=True,null=True)
    
    # unit_charges=ArrayField(models.IntegerField(blank=True, null=True, default=[]))

    create_nos = models.IntegerField(blank=True, null=True)
    random_id = models.CharField(max_length=45, blank=True, null=True)

    occupancy_status = models.CharField(
    max_length=20, blank=True, null=True, default="vacant")
    past_status = models.CharField(
    max_length=20, blank=True, null=True, default="vacant")
    occupied_by = models.IntegerField(blank=True, null=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='unit_added_by',null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    objects=UnitManager()
    def __str__(self):
        return f"{self.unit_name}, {self.unit_property.property_name} "
    class Meta:
         verbose_name_plural = "Units"
         ordering = ['unit_property','create_nos']
    def get_absolute_url(self):
        return reverse("property:unit-detail", args=[self.id])


class Unit_features(models.Model):
    name =models.CharField(max_length=35,blank=True, null=True)
    created_at=models.CharField(max_length=35,blank=True, null=True,default="none")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='features_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.name} "
class Unit_photos(models.Model):
    photo=models.ImageField(upload_to='units',null=True)
    created_at=models.CharField(max_length=35,blank=True, null=True,default="none")
    name=models.CharField(max_length=50)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='photos_added_by')
    added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.name} "
class Property_documents(models.Model):
    property=models.ForeignKey(Property, on_delete=models.SET_NULL, null=True,blank=True,related_name='property_document_property')
    document=models.FileField(upload_to='property',null=True)
    category=models.CharField(max_length=50, default="document")
    random_value=models.CharField(max_length=50, null=True,blank=True)
    created_at=models.CharField(max_length=35,blank=True, null=True,default="none")
    name=models.CharField(max_length=50)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='property_document_added_by')
    added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.name} "
class Utility_bills(models.Model):
    property=models.ForeignKey(Property, on_delete=models.SET_NULL, null=True,blank=True,related_name='property_utility')
    random_value=models.CharField(max_length=50, null=True,blank=True)
    name=models.CharField(max_length=50)
    amount=models.IntegerField(default=0)
    group=models.CharField(max_length=50,default="expense")
    category=models.CharField(max_length=50,blank=True, null=True)
    duration = models.CharField(max_length=35,blank=True, null=True)
    once_date = models.DateField(blank=True, null=True)
    week_date = models.CharField(max_length=15,blank=True, null=True)
    month_date = models.IntegerField(blank=True, null=True,default=0)

    year_date = models.CharField(max_length=15,blank=True, null=True)
    year_day = models.IntegerField(blank=True, null=True)
    year_month = models.CharField(max_length=15,blank=True, null=True)

    expected_by = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='utility_added_by')
    added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def save(self,*args,**kwargs):
        if self.group!="custom":
            self.category=self.group
        if self.group=="tax":
            self.year_day=self.year_date.split(",")[0]
            self.year_month=self.year_date.split(",")[1]
            self.month_date=None
          
        return super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.name} "



