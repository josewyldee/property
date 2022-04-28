from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cost, Maintenance
from finance.models import Expense

@receiver(post_save, sender=Cost)
def lease_post_save(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    print('AAAAAAAAFTER')

    # print('unit',unit_id)
    # print('tenant',tenant_id)
    # print('innnnnnnnnnnnnnnnnstANCE',instance.document.url)
    if created:
       
        ("signals **********************************")
        print(instance.cost_name,' ',instance.cost_total)
        print("signals **********************************")
        m = Maintenance.objects.get(id=instance.maintenance.id)
        unit=m.unit
        property=m.unit.unit_property
        print(unit)
        # tenant.update(occupancy_status="occupied")
        # unit = Unit.objects.filter(id=unit_id)
        # unit.update(occupancy_status="occupied")
        # message=f'A {instance.lease_type} lease was created'  
        if instance.paid=="paid":
            Expense.objects.create(property=property,unit=unit,payee=instance.payee,expense_name=instance.cost_name,description=instance.cost_description,amount=instance.cost_total,created_on=instance.paid_date,ref_no=instance.ref_no,paid_through=instance.paid_through,added_by=instance.added_by,data_type="maintenanace",data_id=instance)
        # if tenant[0].user:
        #     Notification.objects.create(lease=instance,message=message,notification_type='lease',from_user=instance.added_by,to_user=tenant[0].user)
    else:
        if instance.paid=="paid":
            m = Maintenance.objects.get(id=instance.maintenance.id)
            unit=m.unit
            property=m.unit.unit_property
        
            Expense.objects.filter(data_id=instance).delete()
            Expense.objects.create(property=property,unit=unit,payee=instance.payee,expense_name=instance.cost_name,description=instance.cost_description,amount=instance.cost_total,created_on=instance.paid_date,ref_no=instance.ref_no,paid_through=instance.paid_through,added_by=instance.added_by,data_type="maintenanace",data_id=instance)
     
        print("data was updated")



