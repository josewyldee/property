# Generated by Django 4.0 on 2022-02-14 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_payment_options_added_by_payment_options_added_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_options',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
