from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Tenant,Lease,LeaseTermination,TenantDocuments
from property.models import Unit
from customAuth.models import User
from finance.models import Statement,Invoice,Receipt
from finance.utils import generate_transaction_id
# from notifications.models import Notification

@receiver(post_save, sender=Lease)
def lease_post_save(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    print('AAAAAAAAFTER')
    unit_id=instance.unit.id
    tenant_id=instance.tenant.id
    # print('unit',unit_id)
    # print('tenant',tenant_id)
    # print('innnnnnnnnnnnnnnnnstANCE',instance.document.url)
    unit = Unit.objects.filter(id=unit_id)
    if instance.lease_group=="purchase":
        unit.update(occupancy_status="sold")
    else:
        unit.update(occupancy_status="rented")

    if created:
        tenant = Tenant.objects.filter(id=tenant_id)
        tenant.update(occupancy_status="occupied")
        unit = Unit.objects.filter(id=unit_id)
        
        message=f'A {instance.lease_type} lease was created'  
        name="lease"
        if instance.lease_group=="purchase":
            name="receipt"
            lease=instance
            lease_id=instance.id
            transaction_id=generate_transaction_id()
            invoice_group=f'INV{lease_id}{transaction_id}'
            receipt_group=f'RCPT{lease_id}{transaction_id}'
            amount=instance.purchase_price
            created_on=instance.start_date
            added_by=instance.added_by
            ref_no=instance.ref_no
            paid_through=instance.paid_through
            created_time='12:13:12'
            statement_instance_invoice=Statement.objects.create(statement_invoice=invoice_group,lease=lease,type='invoice',amount=amount,amount_sorted=amount,created_on=created_on,added_by=added_by)
            invoice_instance=Invoice.objects.create(added_on=created_on
                    ,lease=lease
                    ,invoice_group=statement_instance_invoice,invoice_group_bulk=transaction_id
                   ,name="Property sale"
                    ,amount=amount,amount_sorted=amount,communication='not sent'
                    ,description='Property was sold'
                    ,created_on=created_on,added_by=added_by
                    )
            statement_instance_receipt=Statement.objects.create(statement_receipt=receipt_group,lease=lease,type='payment',amount=amount,created_on=created_on,added_by=added_by)
            receipt_instance=Receipt.objects.create(added_on=created_on
                         ,lease=lease
                        ,receipt_group=statement_instance_receipt,is_prepayment=False
                        ,amount=amount,communication='not sent'
                        ,description='Property sold',invoice=invoice_instance
                        ,ref_no=ref_no,paid_through=paid_through
                        ,created_on=created_on,created_time=created_time,added_by=added_by
                        
                        )
            unit.update(occupancy_status="sold")
        else:
            unit.update(occupancy_status="rented")

        TenantDocuments.objects.create(name=name,tenant=instance.tenant,document=instance.document.url,added_by=instance.added_by)
        # if tenant[0].user:
        #     Notification.objects.create(lease=instance,message=message,notification_type='lease',from_user=instance.added_by,to_user=tenant[0].user)
    else:

        TenantDocuments.objects.create(name="Lease",tenant=instance.tenant,document=instance.document.url,added_by=instance.added_by)
        print("data was updated")

@receiver(post_save, sender=LeaseTermination)
def lease_post_save(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    print('AAAAAAAAFTER')

    if created:
       
        lease = Lease.objects.get(id=instance.lease.id)
        lease.active=False
        lease.save()

        tenant = Tenant.objects.get(id=lease.tenant.id)
        tenant.occupancy_status="no unit"
        tenant.save()
        if tenant.user:
            account=User.objects.get(id=tenant.user.id)
            account.is_active=False
            account.save()


        unit = Unit.objects.get(id=lease.unit.id)
        unit.occupancy_status="vacant"
        unit.save()
        message=f'A lease was terminated'  
        # if tenant.user:
        #     Notification.objects.create(lease=instance.lease,message=message,notification_type='lease',from_user=instance.added_by,to_user=tenant.user)
    else:
        print('aaaaaaaaaaaaaaaaaaaaaargh')
        print('instance not created')