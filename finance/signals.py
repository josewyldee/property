from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Invoice


@receiver(post_save, sender=Invoice)
def lease_post_save(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    print('AAAAAAAAFTER')

    # print('unit',unit_id)
    # print('tenant',tenant_id)
    # print('innnnnnnnnnnnnnnnnstANCE',instance.document.url)
    if created:
       
        ("signals **********************************")
        print(instance.name,' ',instance.amount)
        print("signals **********************************")
        # tenant = Tenant.objects.filter(id=tenant_id)
        # tenant.update(occupancy_status="occupied")
        # unit = Unit.objects.filter(id=unit_id)
        # unit.update(occupancy_status="occupied")
        # message=f'A {instance.lease_type} lease was created'  
        # if tenant[0].user:
        #     Notification.objects.create(lease=instance,message=message,notification_type='lease',from_user=instance.added_by,to_user=tenant[0].user)
    else:


        print("data was updated")



