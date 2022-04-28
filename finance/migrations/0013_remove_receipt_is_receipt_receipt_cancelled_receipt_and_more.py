# Generated by Django 4.0 on 2022-02-09 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_remove_invoice_is_invoice_invoice_invoice_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='is_receipt',
        ),
        migrations.AddField(
            model_name='receipt',
            name='cancelled_receipt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoice_debitnote', to='finance.receipt'),
        ),
        migrations.AddField(
            model_name='receipt',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='receipt',
            name='receipt_type',
            field=models.CharField(default='payment', max_length=25),
        ),
    ]
