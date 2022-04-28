from django.db import models
from django.conf import settings
User=settings.AUTH_USER_MODEL
from tenant.models import Lease


# Create your models here.
class Email(models.Model):
    subject=models.CharField(max_length=50)
    body=models.TextField(max_length=500)
    group=models.CharField(max_length=25,default='normal')
    type=models.CharField(max_length=25,default='normal')
    type_id=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=15,default='not sent')
    document=models.FileField(upload_to='communication', null=True,blank=True)
    reason=models.CharField(max_length=25,null=True,blank=True)
    email_sent_to=models.EmailField(null=True,blank=True)
    lease=models.ForeignKey(Lease, on_delete=models.CASCADE,null=True,blank=True)
    added_on = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='email_added_by')
    class Meta:
        ordering = ['-added_on']
    def __str__(self):
        return f"Type:{self.type},Subject:{self.subject}"