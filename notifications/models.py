from django.db import models
from django.conf import settings
from maintenance.models import Maintenance
from finance.models import Expense, Statement
# from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save


from tenant.models import Lease, Tenant

User=settings.AUTH_USER_MODEL
# Create your models here.
class Notification(models.Model):
	# 1 = Miantenanance, 2 = Normal, 3 = lease
	notification_type = models.CharField(max_length=15,default="normal")
	title=models.CharField(max_length=50,blank=True,null=True)
	message=models.TextField(blank=True,null=True)

	to_group=models.CharField(default="tenant", max_length=15)
	to_id=models.IntegerField(blank=True,null=True)
	
	from_group=models.CharField(default="system", max_length=15)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True,blank=True)

	maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	statement=models.ForeignKey(Statement, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='+', blank=True, null=True)

	date = models.DateTimeField(default=timezone.now)
	status = models.CharField(default="unread", max_length=10)
	added_on = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		ordering = ['-status', '-date']
	@property
	def since(self):
		date_diff=(timezone.now() - self.date).days     
		return date_diff

	# @receiver(post_save, sender=Maintenance)

	# def create_maintenance_instace(sender, instance, created, **kwargs):
		
	# 	tenant=Tenant.objects.get(id=instance.tenant.id)

	# 	if created:
	# 		message=f' {instance.name}  issue was reported' 
	# 		to_user=tenant.user
	# 		Notification.objects.create(maintenance=instance,message=message,notification_type='maintenance',from_user=instance.added_by,to_user=to_user,date=instance.reported_on)
	# 	else:
	# 			print("oooooooooooooops, not an admin")



