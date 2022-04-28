
from django.db.models import Q
from django.db import models
class GeneralQuerySet(models.QuerySet):
    def filtered_view(self,lookups=None):
        if lookups is None:
            return self.none()
        return self.filter(lookups)
    
    def select_tenants_email(self,lookups=None):
        data=self.filter(lookups).select_related('unit','tenant')
        output= []
        for row in data:
            if row.tenant.email:
              output.append(f'<option data-subtext="(from {row.unit.unit_name})" value="{row.id}">{row.tenant.name} </option>')  
            # output.append(f'<option  value="{row.id}">{row.name}</option>')        
        return output
    def create_invoice_unit(self,lookups=None):
        data=self.filter(lookups).select_related('unit','tenant')
        output= []
        for row in data:
            output.append(f'<option data-subtext="(from {row.unit.unit_name})" value="{row.id}">{row.tenant.name} </option>')  

            # output.append(f'<option value="{row.id}">{row.tenant.name} ({row.unit.unit_name}, {row.unit.unit_property.property_name})</option>')  
            # output.append(f'<option  value="{row.id}">{row.name}</option>')        
        return output
    def select_option_tenants(self,lookups=None):
        data=self.filter(lookups)
        output= ['<option selected="" disabled="">Select a tenant</option>']
        for row in data:
            output.append(f'<option  value="{row.id}">{row.name}</option>')        
        return output
    def select_option_tenants_lease(self,lookups=None):
        data=self.filter(lookups)
        output= ['<option selected="" disabled="">Select a tenant</option>']
        for row in data:
            output.append(f'<option  value="{row.id}">{row.name}</option>')        
        return output
    def select_option_buyers(self,lookups=None):
        data=self.filter(lookups)
        output= ['<option selected="" disabled="">Select a buyer</option>']
        for row in data:
            output.append(f'<option  value="{row.id}">{row.name}</option>')        
        return output
    def select_option_unit_maintenance(self,lookups=None):
        if lookups==None:
            data=self
        else:
            data=self.filter(lookups)

        if data:
            output= ['<option selected="" disabled="">select a property</option>']
            for row in data:
                output.append(f'<option value="{row.tenant.id},{row.unit.id}">{row.unit.unit_name} ({row.tenant.name}) </option>') 
        else:
            output= ['<option selected="" disabled="" class="text-danger">Ooops no records found (hint: allocate a unit to a tenant)</option>']
               
        return output
    def select_option_lease(self,lookups=None):
        data=self.filter(lookups)
        if data:
            output= ['<option selected="" disabled="">Select a lease</option>']
            for row in data:
                output.append(f'<option value="{row.id},{row.unit.id},{row.tenant.id}">{row.unit.unit_name} ({row.tenant.name}) </option>') 
        else:
            output= ['<option selected="" disabled="" class="text-danger">There are no active lease</option>']
               
        return output


class TenantManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
    def filtered_view(self,name=None,user=None,occupancy_status=None,tenant=None):
        query = Q()
        if name is not None:
            query &= Q(name__startswith=name)
        if user is not None:
            query &= Q(added_by=user)
        if occupancy_status is not None:
            query &= Q(occupancy_status=occupancy_status)
        if tenant is not None:
            query &= Q(tenant=tenant)
        
        lookups=Q(query)
        return self.get_queryset().filtered_view(lookups=lookups)
    def only_tenants(self,tenant=None):
        if tenant is not None:
            query = Q(tenant=tenant)
        return self.get_queryset().filtered_view(lookups=query)
    def select_option_tenants(self,tenant=None,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        query = Q()
        if tenant is not None:
            query = Q(id=tenant)
        if not is_syestem_admin:
            query = Q(added_by=user)
        return self.get_queryset().select_option_tenants(lookups=query)
    def select_option_tenants_lease(self,tenant=None,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        query = Q()
        if tenant is not None:
            query = Q(id=tenant)
        if not is_syestem_admin:
            query = Q(added_by=user)
        query=Q(tenant_type="renter")
        return self.get_queryset().select_option_tenants_lease(lookups=query)
    def select_option_buyers(self,tenant=None,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        query = Q()
        if tenant is not None:
            query = Q(id=tenant)
        if not is_syestem_admin:
            query = Q(added_by=user)
        query=Q(tenant_type="buyer")
        
        return self.get_queryset().select_option_buyers(lookups=query)


    def select_option_tenants_account(self,tenant=None,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        query = Q()
        if tenant is not None:
           query &= Q(id=tenant)
        query &= Q(user__isnull=True)
    
        return self.get_queryset().select_option_tenants(lookups=query)
    def select_option_unit_maintenance(self,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        # query = Q()

        # if not is_syestem_admin:
        #     query = Q(added_by=user)
        return self.get_queryset().select_option_unit_maintenance()
    
class LeaseManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)

    def select_option_unit_maintenance(self,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        # query = Q()

        # if not is_syestem_admin:
        #     query = Q(added_by=user)
        return self.get_queryset().select_option_unit_maintenance()
    def select_option_lease(self,user=None,is_syestem_admin=False):
        # print(f'tenant {tenant}, user{user} client {user_type}')
        query = Q()

        if not is_syestem_admin:
            query = Q(added_by=user)
        query &= Q(active=True)
        return self.get_queryset().select_option_lease(lookups=query)
    def create_invoice_unit(self,user=None,is_syestem_admin=False,property=None):
        query = Q()
        if property is not None:
            if property!='all':
                query &= Q(unit__unit_property__in=property)

        # if not is_syestem_admin:
        #     query &= Q(added_by=user)
        # query &= Q(occupancy_status='occupied')
     
        return self.get_queryset().create_invoice_unit(lookups=query)
    def select_tenants_email(self,user=None,is_syestem_admin=False,property=None):
        query = Q()
        print("thhhhhhhhhhhhe property",property)
        if property is not None:
            if property!='all':
                query &= Q(unit__unit_property__in=property)

        if not is_syestem_admin:
            query &= Q(added_by=user)
        # query &= Q(occupancy_status='occupied')
     
        return self.get_queryset().select_tenants_email(lookups=query)
