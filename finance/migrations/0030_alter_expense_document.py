# Generated by Django 4.0 on 2022-02-26 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0029_alter_expense_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='document',
            field=models.ImageField(null=True, upload_to='expense'),
        ),
    ]
