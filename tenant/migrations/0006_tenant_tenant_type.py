# Generated by Django 4.0 on 2022-02-27 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0005_lease_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='tenant_type',
            field=models.CharField(default='renter', max_length=25),
        ),
    ]