# Generated by Django 4.0 on 2022-02-06 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='paid_through',
            field=models.CharField(default='cash', max_length=25),
        ),
        migrations.AddField(
            model_name='cost',
            name='ref_no',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
