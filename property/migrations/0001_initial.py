# Generated by Django 4.0 on 2022-01-31 16:42

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=35)),
                ('property_category', models.CharField(default='Residential', max_length=35)),
                ('property_type', models.CharField(default='Apartment buildings', max_length=35)),
                ('year_created', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(default='Kenya', max_length=50)),
                ('city', models.CharField(default='Nairobi', max_length=50)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('landmark_description', models.TextField(blank=True, max_length=350, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('photo', models.ImageField(default='property/building.jpg', upload_to='property')),
                ('description', models.TextField(blank=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_added_by', to='customAuth.user')),
                ('managed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_manager', to='customAuth.user')),
                ('owned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_owner', to='customAuth.user')),
            ],
            options={
                'verbose_name_plural': 'Buildings',
                'ordering': ['added_on'],
            },
        ),
        migrations.CreateModel(
            name='Unit_photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='units')),
                ('created_at', models.CharField(blank=True, default='none', max_length=35, null=True)),
                ('name', models.CharField(max_length=50)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='photos_added_by', to='customAuth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Unit_features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=35, null=True)),
                ('created_at', models.CharField(blank=True, default='none', max_length=35, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='features_added_by', to='customAuth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=35)),
                ('unit_category', models.CharField(default='Residential', max_length=35)),
                ('unit_type', models.CharField(blank=True, max_length=35, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('baths', models.CharField(blank=True, max_length=10, null=True)),
                ('is_furnished', models.CharField(default='yes', max_length=5)),
                ('water_mtr', models.CharField(blank=True, max_length=45, null=True)),
                ('electricity_mtr', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('bedrooms', models.IntegerField(default=1)),
                ('unit_charges', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('unit_features', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('unit_photos', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('create_nos', models.IntegerField(blank=True, null=True)),
                ('random_id', models.CharField(blank=True, max_length=45, null=True)),
                ('occupancy_status', models.CharField(blank=True, default='vacant', max_length=20, null=True)),
                ('past_status', models.CharField(blank=True, default='vacant', max_length=20, null=True)),
                ('occupied_by', models.IntegerField(blank=True, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_added_by', to='customAuth.user')),
                ('unit_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
            options={
                'verbose_name_plural': 'Units',
                'ordering': ['unit_property', 'create_nos'],
            },
        ),
    ]
