# Generated by Django 4.0 on 2022-02-06 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0002_cost_paid_through_cost_ref_no'),
        ('finance', '0007_alter_expense_payee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='data_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maintenance.cost'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='status',
            field=models.CharField(default='paid', max_length=10),
        ),
    ]
