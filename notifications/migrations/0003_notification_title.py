# Generated by Django 4.0 on 2022-02-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notification_from_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]