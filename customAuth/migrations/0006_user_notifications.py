# Generated by Django 4.0 on 2022-02-19 18:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customAuth', '0005_alter_payee_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notifications',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, null=True, size=None),
        ),
    ]