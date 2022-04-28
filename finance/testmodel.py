from django.db import models
from django.conf import settings
from.managers import LateFeeManager
from property.models import Property, Unit
from tenant.models import Tenant
from customAuth.models import Payee
import datetime
# from django.contrib.auth.models import User


User=settings.AUTH_USER_MODEL

class Charges(models.Model):
    # unit_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=35,blank=True, null=True)
    category = models.CharField(max_length=35)
    amount =models.IntegerField(blank=True, null=True)
    notify = models.CharField(max_length=35,blank=True, null=True,default="none")
    duration = models.CharField(max_length=35,blank=True, null=True)
    once_date = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    week_date = models.CharField(max_length=15,blank=True, null=True)
    month_date = models.IntegerField(blank=True, null=True)

    year_date = models.CharField(max_length=15,blank=True, null=True)
    year_day = models.IntegerField(blank=True, null=True)
    year_month = models.CharField(max_length=15,blank=True, null=True)
    created_at=models.CharField(max_length=35,blank=True, null=True,default="none")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='charges_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def save(self,*args,**kwargs):
        if self.category != "custom":
            self.name=self.category
        if self.duration=="annually":
            self.year_day=self.year_date.split(",")[0]
            self.year_month=self.year_date.split(",")[1]
        return super().save(*args,**kwargs)

    
    def __str__(self):
        return f"{self.name}, {self.amount} , {self.duration}"


class statement(models.Model):
    # invoice_group = models.ForeignKey(Invoice, to_field="invoice", db_column="invoice_group",on_delete=models.PROTECT,null=True ,blank=True)

    statement_invoice=models.CharField(max_length=50,unique=True)
    statement_receipt=models.CharField(max_length=50)
    type=models.CharField(max_length=15,blank=True, null=True)
    amount=models.IntegerField(blank=True, null=True,default=0)
    amount_sorted=models.IntegerField(blank=True, null=True,default=0)
    created_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='statement_added_by')
    class Meta:
        ordering = ['-created_on']


   
class Invoice(models.Model):
    # invoice_group = models.ForeignKey(statement, to_field="statement_invoice", db_column="statement_invoice",on_delete=models.CASCADE,null=True ,blank=True)
    invoice_group=models.CharField(max_length=50,null=True,blank=True)
    invoice_group_bulk=models.CharField(max_length=50)
    is_invoice=models.BooleanField(default=True)
    invoice_duration=models.CharField(max_length=25,default="once")
    name=models.CharField(max_length=25,blank=True, null=True)
    

    amount=models.IntegerField(default=0)

    tenant=models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True,blank=True)
    unit=models.ForeignKey(Unit, on_delete=models.PROTECT,null=True,blank=True)
    property=models.ForeignKey(Property, on_delete=models.PROTECT,null=True,blank=True)

    communication=models.CharField(max_length=25,default="None")
    description=models.CharField(max_length=500,blank=True, null=True)
    currency=models.CharField(max_length=5,default="USD")
    
    late_fee=models.BooleanField(default=False)
    deadline=models.CharField(default='yes',max_length=10)
    late_fee_category=models.CharField(default='generic',max_length=10,blank=True, null=True)
    deadline_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    late_fee_invoice=models.ForeignKey("self",on_delete=models.PROTECT,blank=True, null=True)
    late_fee_type=models.CharField(max_length=30,blank=True, null=True)
    late_fee_grace=models.IntegerField(blank=True, null=True)
    late_fee_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    late_fee_max=models.IntegerField(default=0,blank=True, null=True)
    late_fee_amount=models.IntegerField(blank=True, null=True)

    created_on = models.DateField(auto_now=False, auto_now_add=True,blank=True, null=True)
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='invoice_added_by')
    created_by=models.CharField(default="user",max_length=10)
  
    def save(self,*args,**kwargs):
        print("save model--------------------------")
        print(self.name,' ',self.amount)
        print("save model--------------------------")
        # self.invoice_group_bulk+=1
        # if self.late_fee:
            
        #     self.deadline_date = datetime.date.today() + datetime.timedelta(days=self.late_fee_grace)

        return super().save(*args,**kwargs)
    class Meta:
        ordering = ['-created_on']
    
class Expense(models.Model):
    expense_category=models.CharField(max_length=40,null=True,blank=True)
    expense_name=models.CharField(max_length=40,null=True,blank=True)
    amount=models.IntegerField(default=0)
    created_for=models.CharField(default="building",max_length=10)
    payee=models.ForeignKey(Payee, on_delete=models.SET_NULL,null=True,blank=True)
    unit=models.ForeignKey(Unit, on_delete=models.SET_NULL,null=True,blank=True)
    property=models.ForeignKey(Property, on_delete=models.SET_NULL,null=True,blank=True)
    description=models.CharField(max_length=500,blank=True, null=True)
    status=models.CharField(default="not paid",max_length=10)

    paid_through=models.CharField(max_length=10,default="cash")
    paid_through_name=models.CharField(max_length=45,null=True,blank=True)
    paid_through_number=models.IntegerField(blank=True, null=True)
    paid_through_reference=models.CharField(blank=True, null=True,max_length=45)
    created_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='expense_added_by')
    class Meta:
        ordering = ['-created_on']







class Receipt(models.Model):
    receipt=models.IntegerField()
    receipt_group=models.IntegerField()

    is_receipt=models.BooleanField(default=True)

    # for_invoice = models.ForeignKey(Invoice, to_field="invoice", db_column="invoice_group",on_delete=models.PROTECT,null=True ,blank=True)
    for_invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE,null=True,blank=True)
 

    amount=models.IntegerField(default=0)
    tenant=models.ForeignKey(Tenant, on_delete=models.PROTECT,null=True,blank=True)
    Unit=models.ForeignKey(Unit, on_delete=models.PROTECT,null=True,blank=True)
    property=models.ForeignKey(Property, on_delete=models.PROTECT,null=True,blank=True)

    ref_no=models.CharField(max_length=45,null=True,blank=True)
    paid_through=models.CharField(max_length=10,default="cash")
    paid_through_name=models.CharField(max_length=45,null=True,blank=True)
    paid_through_number=models.IntegerField(blank=True, null=True)
    paid_through_reference=models.CharField(blank=True, null=True,max_length=45)

    communication=models.CharField(max_length=25,default="None")
    description=models.CharField(max_length=500,blank=True, null=True)
    currency=models.CharField(max_length=5,default="USD")

    created_on = models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='receipt_added_by')
    created_by=models.CharField(default="user",max_length=10)
    class Meta:
        ordering = ['-created_on']
    
class Late_fee_types(models.Model):
    name=models.CharField(max_length=50)
    value=models.CharField(max_length=50)
    duration=models.CharField(max_length=50,default='once')
    created_for=models.CharField(max_length=50,default='everyone')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,related_name='laet_fee_added_by')
    added_on = added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    objects=LateFeeManager()


   


    