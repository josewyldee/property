# Generated by Django 4.0 on 2022-02-26 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0033_alter_charges_amount_alter_charges_late_fee_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charges',
            name='late_fee_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='amount_late_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='amount_sorted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='late_fee_max',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
