# Generated by Django 4.0 on 2022-02-13 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0002_property_country_code'),
        ('finance', '0014_alter_invoice_cancelled_invoice_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('account_info', models.CharField(blank=True, max_length=50, null=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_option_property', to='property.property')),
            ],
        ),
    ]
