from django.db import models
from tenant.models import Tenant
from property.models import Unit
from django.conf import settings
import datetime
from django.db.models.signals import post_save
from customAuth.models import Payee

User=settings.AUTH_USER_MODEL

class Maintenance(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,null=True,blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,null=True,blank=True)
    priority = models.CharField(max_length=35,default="normal")
    name = models.CharField(max_length=35,null=True,blank=True)
    category = models.CharField(max_length=35)
    description=models.TextField(null=True,blank=True)
    reported_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    solved_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    status=models.CharField(max_length=35,default="not started")
    urgency=models.CharField(max_length=20,default="not urgent")
    
    
    opened=models.BooleanField(default=False)
    added_by_category = models.CharField(max_length=35,default="admin")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='maintenance_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    @property
    def since(self):
        date_diff=( datetime.date.today() - self.reported_on).days     
        return date_diff
    def save(self,*args,**kwargs):
        if self.category != "custom":
            self.name=self.category

        return super().save(*args,**kwargs)



    def __str__(self):
        return f"{self.name}, {self.reported_on}, {self.status}"
    class Meta:
        ordering = ["-reported_on"]
        
class Cost(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    cost_type=models.CharField(max_length=35,default="materials")
    cost_name=models.CharField(null=True,blank=True,max_length=35)
    cost_number=models.IntegerField(default=1)
    cost_description=models.TextField(null=True,blank=True)
    cost_total=models.IntegerField()
    payee=models.ForeignKey(Payee, on_delete=models.CASCADE,null=True,blank=True)
    paid=models.CharField(max_length=10,default="not paid")
    paid_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    paid_by=models.CharField(max_length=10,default="us")
    ref_no=models.CharField(max_length=45,null=True,blank=True)
    paid_through=models.CharField(max_length=25,default="cash")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='cost_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.cost_type}, {self.cost_name} {self.cost_total}"
class Document(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    document=models.ImageField(upload_to='maintenane',null=True)
    name=models.CharField(null=True,blank=True,max_length=35)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='document_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.name}"



