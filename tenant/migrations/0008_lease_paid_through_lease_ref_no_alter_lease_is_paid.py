# Generated by Django 4.0 on 2022-02-27 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0007_lease_is_paid_lease_lease_group_lease_purchase_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease',
            name='paid_through',
            field=models.CharField(default='cash', max_length=25),
        ),
        migrations.AddField(
            model_name='lease',
            name='ref_no',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='lease',
            name='is_paid',
            field=models.BooleanField(default='no', max_length=5),
        ),
    ]
