from django.conf import settings
from django.db.models import Q
from django.db import models
from .models import User

User=settings.AUTH_USER_MODEL
def select_option_admin():
    data = User.objects.filter(is_syestem_admin=True)
    output= []
    for row in data:
        output.append(f'<option data-subtext="(Admin)" value="{row.id}">{row.username} </option>')        
    return output

class GeneralQuerySet(models.QuerySet):


    def select_payees(self,lookups=None):
        data=self.filter(lookups)
        
        output= ['<option selected="" disabled="">Select a payees</option>']
        for row in data:
            output.append(f'<option  value="{row.id}">{row.name}</option>')  
        output.append('<option class="text-primary fancy_text4" value="add_payee">Click to add</option>')      
        return output
 

 
class PayeeManager(models.Manager):
    def get_queryset(self):
        return GeneralQuerySet(self.model,using=self.db)
 

    def select_payees(self,is_syestem_admin=False,user=None):
        query = Q()
        query &= Q(added_by=user)
        return self.get_queryset().select_payees(lookups=query)
   
    
