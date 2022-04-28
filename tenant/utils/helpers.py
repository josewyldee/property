from django.db import models

class commonModel(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True
        # ordering=('added_on',)
class peopleModel(models.Model):
    category_choices = (
        ('company', 'Company'),
        ('individual', 'Individual'),
    )
    email = models.EmailField(max_length=255, blank=True,null=True)
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=15, choices=category_choices, default='individual')
    calling_code = models.PositiveIntegerField(default=254)
    phone_number = models.BigIntegerField(blank=True,null=True)
    class Meta:
        abstract=True
        # ordering=('added_on',)