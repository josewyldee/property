from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from tenant.utils.helpers import peopleModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from finance.managers import PayeeManager
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    is_syestem_admin = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)
    notifications = ArrayField(models.CharField(max_length=500), blank=True,null=True)
    objects = UserManager()



class Payee(peopleModel):
    website = models.CharField(max_length=50,blank=True,null=True)
    company_name=models.CharField(max_length=50,blank=True,null=True)
    payee_category=models.CharField(max_length=50,blank=True,null=True)
    description=models.CharField(max_length=500,blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='payee_added_by')
    objects=PayeeManager()
    class Meta:
        ordering = ['name']

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True,related_name="profile_user")
    name = models.CharField(max_length=50, blank=True,null=True)
    image=models.ImageField(upload_to='profile',default="profile/no_profile.jpg")
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='admin_added_by',null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if instance.is_superuser:
                AdminProfile.objects.create(user=instance)
            else:
                print("oooooooooooooops, not an admin")

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     if instance.is_superuser:
    #         instance.save()
    #     else:
    #         print("oooooooooooooops, not save an admin")

    @property
    def get_full_name(self):
        return self.name
    @property
    def get_first_name(self):
        return self.name.split()[0]
    @property
    def get_last_name(self):
        if self.name.split()[1]:
            return self.name.split()[1]
        return self.name.split()[0]