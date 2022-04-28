from django.db import models
from .utils.helpers import peopleModel
from django.conf import settings
from .managers import TenantManager,LeaseManager
# from django.contrib.auth.models import User
from property.models import Unit
User=settings.AUTH_USER_MODEL



class Tenant(peopleModel):
    user = models.OneToOneField(User,
                                unique=True,
                                db_index=True,
                                related_name='tenant_user',
                                blank=True, null=True,
                                on_delete=models.CASCADE)
    occupancy_status = models.CharField(max_length=25, default="no unit")
    is_active = models.CharField(max_length=10,default="Active")
    image=models.ImageField(upload_to='profile',default="profile/no_profile.jpg")
    timeline_type = models.CharField(max_length=25, default="current")
    tenant_type = models.CharField(max_length=25, default="renter")
    
    nationality = models.CharField(max_length=45, blank=True, null=True)
    proof_by = models.CharField(max_length=25,default="National id")
    
    proof_number = models.IntegerField(blank=True, null=True)
    summary=models.TextField(max_length=250,blank=True, null=True)
    
    random_id = models.CharField(max_length=45, blank=True, null=True)
    
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='tenant_added_by')
    added_on = models.DateTimeField(auto_now_add=True)

    # user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name="tenant_user")

    objects=TenantManager()
    # objects=SelectOptionManager()
    def __str__(self):
        return f'{self.name} {self.occupancy_status} '

    class Meta:
         ordering = ['name']
        # return f'{user.id} - {user.email} - {self.name} {self.current_status}'

class EmergencyContacts(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, blank=True,null=True)
    phone = models.BigIntegerField()
    calling_code = models.PositiveIntegerField(default=254)
    relationship_type=models.CharField(max_length=35,default='family')
    relationship=models.CharField(max_length=55,null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='emergency_added_by',null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} {Tenant.name} '



class Guarantors(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, blank=True,null=True)
    phone = models.BigIntegerField(blank=True,null=True)
    calling_code = models.PositiveIntegerField(default=254)
    relationship_type=models.CharField(max_length=35,default='family')
    relationship=models.CharField(max_length=55,null=True,blank=True)
    has_accepted=models.CharField(default='Not yet',max_length=15)
    notes=models.TextField(max_length=500,null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='guarator_added_by',null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} {Tenant.name} {self.has_accepted}'
    
    
class Lease(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='tenant_lease')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,related_name='unit_lease')
    lease_type=models.CharField(max_length=35,default='fixed period')
    lease_group=models.CharField(max_length=35,default='rent')

    purchase_price=models.IntegerField(default=0)
    is_paid=models.CharField(default="yes",max_length=5)
    paid_through=models.CharField(max_length=25,default="cash")
    ref_no=models.CharField(max_length=45,null=True,blank=True)

    start_date=models.DateField(auto_now=False, auto_now_add=False,blank=False, null=False)
    end_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    document=models.FileField(upload_to='leases')
    sent=models.CharField(max_length=15,default='not sent')
    signed=models.CharField(max_length=15,default='not signed')
    end_lease_notice=models.CharField(max_length=15,default='not sent')
    visible=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    notes=models.TextField(max_length=500,null=True,blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='lease_added_by',null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    objects=LeaseManager()
    def __str__(self):
        return f'{self.tenant.name} {self.unit.unit_name} {self.lease_type}'
class LeaseTermination(models.Model):
    lease = models.OneToOneField(Lease, on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)

    reason=models.CharField(max_length=35,default='End of lease term')
    description=models.TextField(max_length=500,null=True,blank=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='termination_added_by',null=True)
    added_on = models.DateTimeField(auto_now_add=True)


 

    def __str__(self):
        return f'{self.lease.tenant.name} {self.lease.unit.unit_name} {self.reason}'


class TenantDocuments(models.Model):
    name=models.CharField(max_length=50)
    document=models.FileField(upload_to='tenant')
    created_at=models.CharField(max_length=35,blank=True, null=True,default="none")
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='tenant_document_added_by')
    added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"{self.name} "



