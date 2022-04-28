# from django.db.models.signals import pre_save,post_save
# from django.dispatch import receiver
# from .models import Email
# from tenant.models import Lease
# from .utils import Util


# @receiver(pre_save, sender=Email)
# def email_send(sender, instance, *args, **kwargs):
#     data=[]
#     lease=Lease.objects.get(id=instance.lease)
#     if instance.type=="normal":
#         data.append({'subject':instance.subject,'body': instance.body, 'to':instance.email_sent_to,'from':lease.added_by.email,
#                 'name':lease.tenant.name,'property':lease.unit.unit_property.property_name,'document':instance.document})
#     if instance.group=="finanace":
#         if instance.type=="invoice":
#             color="#4b72fa"
#         if instance.type=="credit note":
#             color="#D98880"
#         if instance.type=="receipt":
#             color="#7DCEA0"
#         if instance.type=="debit note":
#             color="#D98880"
#         lease_info=f'{instance.unit.unit_name} {instance.unit.unit_property.property_name} '
#         data.append({'subject':instance.type, 'to':instance.email_sent_to,'from':lease.added_by.email,
#                             'name':lease.tenant.name,'property':lease.unit.unit_property.property_name,'transaction':instance.type,'lease_info':lease_info,'color':color})
        
#     try:
#         Util.send_email(data)
#     except: 
#         instance.save
#     #do something
#     instance.slug = slugify(instance.title)


# @receiver(post_save, sender=Email)
# def lease_post_save(sender,instance,created, **kwargs):
#     print('sender',sender)
#     print('created',created)
#     print('AAAAAAAAFTER')

#     # print('unit',unit_id)
#     # print('tenant',tenant_id)
#     # print('innnnnnnnnnnnnnnnnstANCE',instance.document.url)
#     if created:
#         data=[]
#         if instance.type=="normal":
#             data.append({'subject':subject,'body': body, 'to':email,'from':request.user.email,
#             'name':name,'property':property,'document':document})


#         ("signals **********************************")
#         print(instance.name,' ',instance.amount)
#         print("signals **********************************")
#         # tenant = Tenant.objects.filter(id=tenant_id)
#         # tenant.update(occupancy_status="occupied")
#         # unit = Unit.objects.filter(id=unit_id)
#         # unit.update(occupancy_status="occupied")
#         # message=f'A {instance.lease_type} lease was created'  
#         # if tenant[0].user:
#         #     Notification.objects.create(lease=instance,message=message,notification_type='lease',from_user=instance.added_by,to_user=tenant[0].user)
#     else:


#         print("data was updated")



