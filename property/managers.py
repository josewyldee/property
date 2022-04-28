
from django.db.models import Q,Count
from django.db import models
class GeneralQuerySet(models.QuerySet):
    def filtered_view(self,lookups=None):
        if lookups is None:
            return self.none()
        return self.filter(lookups)

    def select_option_property(self,lookups=None):
        data=self.filter(lookups)
        output= ['<option selected="" disabled="">Select a property</option>']
        for row in data:
            general_name=row.name if row.bulk else f'{row.property_name} in {row.bulk_name}'
            output.append(f'<option data-subtext="{general_name}" value="{row.id},{row.property_name},{row.property_category},{row.property_type}">{row.property_name}</option>')        
        return output
    def select_property(self,lookups=None):
        
        data=self.filter(lookups)
        output= ['<option selected="" disabled="">Select a property</option>']
        for row in data:
   
            output.append(f'<option value="{row.id}">{row.property_name}</option>')        
        return output
    def select_units(self,lookups=None):
        data=self.filter(lookups).select_related('unit_property').order_by("unit_name")
        output= ['<option selected="" disabled="">select a property</option>']
        for row in data:
           
            output.append(f'<option value="{row.id}">{row.unit_name}</option>')        
        return output
    def create_invoice_property(self,lookups=None):
        
        data=self.filter(lookups)
        
        output= []
        # output= ['<option selected="" disabled="">Select a property</option>']
        for row in data:
   
            output.append(f'<option value="{row.id}">{row.property_name}</option>')        
        return output

    def create_invoice_unit(self,lookups=None):
        data=self.filter(lookups).order_by("unit_name")
        output= ['<option selected="" disabled="">select a property</option>']
        for row in data:
           
            output.append(f'<option value="{row.id}">{row.unit_name} </option>')        
        return output



        
    def select_option_property_units(self,lookups=None):
        data=self.filter(lookups).annotate(total_units=Count("unit"))
        
        output= []
        # output= ['<option selected="" disabled="">Select a property</option>']
        for row in data:
            output.append(f'<option value="{row.id},{row.total_units}">{row.property_name}</option>')        
        return output
    def select_option_units(self,lookups=None,except_unit=None):
      
        if except_unit:
            data=self.filter(lookups | Q(id=except_unit)).order_by("unit_property")
        else:
            data=self.filter(lookups).order_by("unit_property")

        output= ['<option selected="" disabled="">select a property</option>']
        for row in data:
            output.append(f'<option value="{row.id}">{row.unit_name} </option>')        
        return output
 
class PropertyManager(models.Manager):
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

    def select_option_property(self,id=None,user=None,user_type='client', role="both"):
        query = Q()
        if user is not None or user_type is not None:
            if id is not None:
                query = Q(id=id)
            if user_type=='client':
                query=Q(added_by=user)
            if role !='both':
                query=Q(role=role)
        else:
            return self.get_queryset().none()
        return self.get_queryset().select_option_property(lookups=query)
    def select_option_property_units(self,property=None,user=None,is_syestem_admin=False):
        query = Q()
        if property is not None:
          
            query &= Q(id=property)

        if not is_syestem_admin:
            query &= Q(added_by=user)
     
        return self.get_queryset().select_option_property_units(lookups=query)

    def create_invoice_property(self,property=None,user=None,is_syestem_admin=False):
        query = Q()
        if property is not None:
          
            query &= Q(id=property)

        if not is_syestem_admin:
            query &= Q(added_by=user)
     
        return self.get_queryset().create_invoice_property(lookups=query)
    def select_property(self,property=None,user=None,is_syestem_admin=False):
        query = Q()
        if property is not None:
          
            query &= Q(id=property)

        # if not is_syestem_admin:
        #     query &= Q(added_by=user)
     
        return self.get_queryset().select_property(lookups=query)
    
    
class UnitManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
   
    def select_option_units(self,status=None,user=None,is_syestem_admin=False,except_unit=None):
        query = Q()

        if status is not None:
            query &= Q(occupancy_status=status)
        if not is_syestem_admin:
            query &= Q(added_by=user)
        


        return self.get_queryset().select_option_units(lookups=query,except_unit=except_unit)

    def create_invoice_unit(self,user=None,is_syestem_admin=False,property=None):
        query = Q()
        if property is not None:
            if property!='all':
                query &= Q(unit_property__in=property)

        if not is_syestem_admin:
            query &= Q(added_by=user)
        query &= Q(occupancy_status='occupied')
     
        return self.get_queryset().create_invoice_unit(lookups=query)
    def select_units(self,user=None,is_syestem_admin=False,property=None):
        query = Q()
        if property is not None:
            if property!='all':
                query &= Q(unit_property__in=property)

        # if not is_syestem_admin:
        #     query &= Q(added_by=user)
        
     
        return self.get_queryset().select_units(lookups=query)
