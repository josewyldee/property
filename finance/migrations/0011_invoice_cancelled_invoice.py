# Generated by Django 4.0 on 2022-02-09 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_alter_expense_paid_through'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cancelled_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoice_creditnote', to='finance.invoice'),
        ),
    ]