# Generated by Django 4.0 on 2022-02-25 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0026_expense_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='document',
            field=models.ImageField(null=True, upload_to='expense'),
        ),
    ]
