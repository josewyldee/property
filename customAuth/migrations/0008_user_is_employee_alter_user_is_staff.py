# Generated by Django 4.0 on 2022-02-20 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customAuth', '0007_alter_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
