# Generated by Django 4.0 on 2022-02-05 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customAuth', '0003_payee_added_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payee',
            options={'ordering': ['name']},
        ),
    ]
