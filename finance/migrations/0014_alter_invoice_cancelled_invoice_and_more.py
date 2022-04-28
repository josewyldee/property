# Generated by Django 4.0 on 2022-02-10 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0013_remove_receipt_is_receipt_receipt_cancelled_receipt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='cancelled_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_creditnote', to='finance.invoice'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='late_fee_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.invoice'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='cancelled_receipt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_debitnote', to='finance.receipt'),
        ),
    ]
