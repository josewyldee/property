# Generated by Django 4.0 on 2022-03-01 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_alter_utility_bills_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utility_bills',
            name='month_date',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
