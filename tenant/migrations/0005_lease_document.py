# Generated by Django 4.0 on 2022-02-25 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0004_lease_end_lease_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease',
            name='document',
            field=models.FileField(default='test', upload_to='leases'),
            preserve_default=False,
        ),
    ]