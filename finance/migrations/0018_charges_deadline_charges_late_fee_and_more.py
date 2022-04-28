# Generated by Django 4.0 on 2022-02-18 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0017_alter_payment_options_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='charges',
            name='deadline',
            field=models.CharField(default='no', max_length=10),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee_category',
            field=models.CharField(blank=True, default='generic', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee_grace',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee_max',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='charges',
            name='late_fee_type',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='deadline',
            field=models.CharField(default='no', max_length=10),
        ),
    ]