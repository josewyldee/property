# Generated by Django 4.0 on 2022-02-25 20:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0025_expense_paid_on_alter_expense_payee'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='document',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='expense'),
            preserve_default=False,
        ),
    ]