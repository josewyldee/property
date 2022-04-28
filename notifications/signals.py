from django.db.models.signals import post_save
from django.dispatch import receiver
from property.models import Unit
from customAuth.models import User
from tenant.models import Tenant
from notifications.models import Notification

@receiver(post_save, sender=Notification)
def lease_post_save(sender,instance,created, **kwargs):
    print('sender',sender)
    print('created',created)
    print('AAAAAAAAFTER')
    print("noooooooooootifications----------------------------")


    if created:
        if instance.to_group=="staff":
            if instance.to_id:
                staff=User.objects.filter(is_tenant=False,id=instance.to_id)
            else:
                staff=User.objects.filter(is_tenant=False)
            i=0
            for r in staff:
                if r.notifications:
                    print("hhhhhhhhhhhhass")
                    notifications_list=r.notifications
                else:
                    notifications_list=[]

                print("preeeeeev",instance.id)
                notifications_list.append(instance.id)
                print("notttifications",notifications_list)
                staff[i].notifications=notifications_list
                staff[i].save()
                i+=1
        
        if instance.to_group=="tenant":
            staff=None
            if instance.to_id:
               
                tenant=Tenant.objects.get(id=instance.to_id)
                if tenant.user:
                    staff=User.objects.filter(is_tenant=True,id=tenant.user.id)
            else:
                staff=User.objects.filter(is_tenant=True)
            i=0
            if staff:
                for r in staff:
                    if r.notifications:
                        print("hhhhhhhhhhhhass")
                        notifications_list=r.notifications
                    else:
                        notifications_list=[]

                    print("preeeeeev",instance.id)
                    notifications_list.append(instance.id)
                    print("notttifications",notifications_list)
                    staff[i].notifications=notifications_list
                    staff[i].save()
                    i+=1
        

        

    else:


        print("data was updated")
