# Generated by Django 4.0 on 2022-03-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_alter_utility_bills_month_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='occupancy_status',
            field=models.CharField(blank=True, default='vacant', max_length=20, null=True),
        ),
    ]