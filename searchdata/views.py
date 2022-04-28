from django.shortcuts import render, HttpResponse
from tenant.models import Tenant,Lease
from property.models import Property,Unit
from finance.models import Late_fee_types, Receipt,Invoice
from customAuth.models import Payee,User
# from customAuth.managers import select_option_admin
import json
def units(request):
    status = request.GET.get('status',None) 
    except_unit = request.GET.get('unit',None) 
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Unit.objects.select_option_units(status=status,user=user,is_syestem_admin=is_syestem_admin,except_unit=except_unit)
    return HttpResponse(data)


def tenants(request):
    tenant = request.GET.get('tenant',None) 
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Tenant.objects.select_option_tenants(tenant=tenant,user=user,is_syestem_admin=is_syestem_admin)
def tenants_lease(request):
    tenant = request.GET.get('tenant',None) 
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Tenant.objects.select_option_tenants_lease(tenant=tenant,user=user,is_syestem_admin=is_syestem_admin)
    return HttpResponse(data)
def buyers(request):
    tenant = request.GET.get('tenant',None) 
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Tenant.objects.select_option_buyers(tenant=tenant,user=user,is_syestem_admin=is_syestem_admin)
    return HttpResponse(data)
def tenants_account(request):
    tenant = request.GET.get('tenant',None) 
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Tenant.objects.select_option_tenants_account(tenant=tenant,user=user,is_syestem_admin=is_syestem_admin)
    return HttpResponse(data)
def unit_maintenance(request):
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Lease.objects.select_option_unit_maintenance(user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)
def lease(request):
    user=None
    is_syestem_admin=request.user.is_superuser
    data=Lease.objects.select_option_lease(user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)
def admin(request):
    
    data = User.objects.filter(is_syestem_admin=True)
    output= []
    for row in data:
        output.append(f'<option data-subtext="(Admin)" value="{row.id}">{row.username} </option>')        
    # return output
    # data=select_option_admin()
    return HttpResponse(output)

    
def property_units(request):
    property = request.GET.get('property',None) 
    # print("martian manhunterrrrr",request.GET.get('property',None) )
   
    user=None
    is_syestem_admin=request.user.is_syestem_admin
    data=Property.objects.select_option_property_units(property=property,user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)
def create_invoice_unit(request):
    user=None
    is_syestem_admin=request.user.is_superuser
    property=json.loads( request.GET.get('property'))
    if property and property!='all':
        property=[int(i) for i in property]
    else:
        property=None
    data=Lease.objects.create_invoice_unit(user=user,is_syestem_admin=is_syestem_admin,property=property)
    return HttpResponse(data)
def select_tenants_email(request):
    user=None
    is_syestem_admin=request.user.is_superuser
    property=json.loads( request.GET.get('property'))
    if property and property!='all':
        property=[int(i) for i in property]
    else:
        property=None
   
    print("suuuuperman222",property )
    data=Lease.objects.select_tenants_email(user=user,is_syestem_admin=is_syestem_admin,property=property)
    return HttpResponse(data)

def create_invoice_property(request):
    property = request.GET.get('property',None) 
 
    user=None
    is_syestem_admin=request.user.is_syestem_admin
    data=Property.objects.create_invoice_property(property=property,user=user,is_syestem_admin=is_syestem_admin)
    return HttpResponse(data)
def select_property(request):
    property = request.GET.get('property',None) 
 
    user=None
    is_syestem_admin=request.user.is_syestem_admin
    data=Property.objects.select_property(property=property,user=user,is_syestem_admin=is_syestem_admin)
    return HttpResponse(data)

def select_units(request):
    user=None
    is_syestem_admin=request.user.is_superuser
    property=json.loads( request.GET.get('property'))
    if property and property!='all':
        property=[int(i) for i in property]
    else:
        property=None
    data=Unit.objects.select_units(user=user,is_syestem_admin=is_syestem_admin,property=property)
    return HttpResponse(data)
def payees(request):
 
    user=request.user.id
    is_syestem_admin=request.user.is_syestem_admin
    data=Payee.objects.select_payees(user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)
def late_fee_types(request):
   
    user=request.user.id
    is_syestem_admin=request.user.is_syestem_admin
    data=Late_fee_types.objects.select_late_fee_type(user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)
def select_invoice(request):
   
    user=request.user.id
    is_syestem_admin=request.user.is_syestem_admin
    data=Invoice.objects.select_invoice(user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)
def select_payment(request):
   
    user=request.user.id
    is_syestem_admin=request.user.is_syestem_admin
    data=Receipt.objects.select_payment(user=user,is_syestem_admin=is_syestem_admin)
 
    return HttpResponse(data)

 