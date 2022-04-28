
from django.db.models import Q,Count
from django.db import models
class GeneralQuerySet(models.QuerySet):
    def select_payees(self,lookups=None):
        if lookups:
            data=self.filter(lookups)
        else:
            data=self
        # data=self.filter(lookups)
        
        output= ['<option selected="" disabled="">Select a payees</option>']
        for row in data:
            output.append(f'<option  value="{row.id}">{row.name}</option>')  
        output.append('<option class="text-primary fancy_text4" value="add_payee">Click to add</option>')      
        return output

    def select_late_fee_type(self,lookups=None):
        data=self.filter(lookups)
        
        output= [
            ''' <option disabled class="disabled_latefee" selected>Select type</option>
                <optgroup label="One time late fee">
                    <option value="one_time_fixed">A fixed amount (Once)</option>
                    <option value="one_time_percent_unpaid">A percentage of only the outstanding invoice (Once)</option>
                    <option value="one_time_percent_entire">A percentage of only the total invoice (Once)</option>
                </optgroup>
                <optgroup label="Daily late fee">
                    <option value="daily_time_fixed">A fixed amount (Daily)</option>
                    <option value="daily_time_percent_unpaid">A percentage of only the outstanding invoice (Daily)</option>
                    <option value="daily_time_percent_entire">A percentage of only the total invoice (Daily)</option>
                </optgroup>
            ''']
        for row in data:
            output.append(f'<option  value="{row.value}">{row.name}</option>')        
        return output
    def select_invoice(self,lookups=None):
        from django.db.models import Sum,OuterRef, Subquery
        data=self.filter(lookups)

        subquery = data.filter(
        invoice_group=OuterRef('invoice_group')
        ).values('invoice_group').annotate(
            total_spent = Sum('amount')
        ).values('total_spent')[:1]

        query = data.annotate(
            total_spent=Subquery(subquery)
        ).select_related("lease","invoice_group").order_by().distinct('invoice_group')

        output= []
        for row in query:
            output.append(f'<option data-subtext="(USD {row.total_spent}  {row.lease.tenant.name})" value="{row.invoice_group.statement_invoice},{row.total_spent},{row.lease.id}">{row.invoice_group.statement_invoice}</option>')        
        return output
    def select_payment(self,lookups=None):
        from django.db.models import Sum,OuterRef, Subquery
        data=self.filter(lookups)

        subquery = data.filter(
        receipt_group=OuterRef('receipt_group')
        ).values('receipt_group').annotate(
            total_spent = Sum('amount')
        ).values('total_spent')[:1]

        query = data.annotate(
            total_spent=Subquery(subquery)
        ).select_related("lease","receipt_group").order_by().distinct('receipt_group')

        output= []
        for row in query:
            output.append(f'<option data-subtext="(USD {row.total_spent} {row.lease.tenant.name})" value="{row.receipt_group.statement_receipt},{row.total_spent},{row.lease.id}">{row.receipt_group.statement_receipt}</option>')        
        return output

    def create_invoice_property(self,lookups=None):
        
        data=self.filter(lookups).annotate(total_units=Count("unit",filter=Q(unit__occupancy_status="occupied")))
        
        output= []
        # output= ['<option selected="" disabled="">Select a property</option>']
        for row in data:
        
            if row.total_units >0:
                output.append(f'<option value="{row.id},{row.total_units}">{row.property_name}</option>')        
        return output

    def create_invoice_unit(self,lookups=None):
        data=self.filter(lookups).order_by("unit_name")
        output= []
        for row in data:
           
            output.append(f'<option value="{row.id}">{row.unit_name}</option>')        
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
            output.append(f'<option value="{row.id}">{row.unit_name}</option>')        
        return output
 
class LateFeeManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
 

    def select_late_fee_type(self,is_syestem_admin=False,user=None):
        query = Q()
        query &= Q(added_by=user)
        return self.get_queryset().select_late_fee_type(lookups=query)

class InvoiceManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
 

    def select_invoice(self,is_syestem_admin=False,user=None):
        query = Q()
        query &= Q(added_by=user)
        query &= Q(invoice_type='invoice')
        query &= Q(is_cancelled=False)
        return self.get_queryset().select_invoice(lookups=query)

class ReceiptManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
 

    def select_payment(self,is_syestem_admin=False,user=None):
        query = Q()
        query &= Q(added_by=user)
        query &= Q(receipt_type='payment')
        query &= Q(is_cancelled=False)
        return self.get_queryset().select_payment(lookups=query)

   
class PayeeManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
 

    def select_payees(self,user=None,is_syestem_admin=False):
        # query = Q()
        # query &= Q(added_by=user)
       
        # return self.get_queryset().select_payees(lookups=query)
        return self.get_queryset().select_payees()
