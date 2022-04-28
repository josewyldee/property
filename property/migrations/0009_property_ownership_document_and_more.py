# Generated by Django 4.0 on 2022-02-27 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customAuth', '0008_user_is_employee_alter_user_is_staff'),
        ('property', '0008_utility_bills_duration_utility_bills_month_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='ownership_document',
            field=models.FileField(default='document', upload_to='property'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='property_authority',
            field=models.CharField(default='Joseph disraeli', max_length=55),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='property_owner',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='property_use',
            field=models.CharField(default='rent', max_length=55),
        ),
        migrations.AddField(
            model_name='utility_bills',
            name='category',
            field=models.CharField(default='expense', max_length=50),
        ),
        migrations.AddField(
            model_name='utility_bills',
            name='group',
            field=models.CharField(default='expense', max_length=50),
        ),
        migrations.AlterField(
            model_name='property',
            name='managed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_manager', to='customAuth.user'),
        ),
        migrations.AlterField(
            model_name='property',
            name='owned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_owner', to='customAuth.user'),
        ),
        migrations.AlterField(
            model_name='property_documents',
            name='document',
            field=models.FileField(null=True, upload_to='property'),
        ),
        migrations.AlterField(
            model_name='utility_bills',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
