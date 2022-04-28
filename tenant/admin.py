from django.contrib import admin
from .models import Tenant,EmergencyContacts,Guarantors,Lease,LeaseTermination,TenantDocuments



@admin.register(Tenant)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('id','name','email','occupancy_status','timeline_type')
@admin.register(Lease)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('id','lease_type','start_date','end_date','active')

@admin.register(EmergencyContacts)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('name','tenant','relationship_type','relationship')

@admin.register(Guarantors)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('name','relationship_type','relationship','has_accepted','tenant')

@admin.register(LeaseTermination)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('lease','reason')
@admin.register(TenantDocuments)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('name',)
