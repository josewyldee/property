# Generated by Django 4.0 on 2022-01-31 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customAuth', '0001_initial'),
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lease_type', models.CharField(default='fixed period', max_length=35)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('sent', models.CharField(default='not sent', max_length=15)),
                ('signed', models.CharField(default='not signed', max_length=15)),
                ('visible', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, max_length=500, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lease_added_by', to='customAuth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('company', 'Company'), ('individual', 'Individual')], default='individual', max_length=15)),
                ('calling_code', models.PositiveIntegerField(default=254)),
                ('phone_number', models.BigIntegerField()),
                ('occupancy_status', models.CharField(default='no unit', max_length=25)),
                ('is_active', models.CharField(default='Active', max_length=10)),
                ('image', models.ImageField(default='profile/no_profile2.jpg', upload_to='profile')),
                ('timeline_type', models.CharField(default='current', max_length=25)),
                ('nationality', models.CharField(blank=True, max_length=45, null=True)),
                ('proof_by', models.CharField(default='National id', max_length=25)),
                ('proof_number', models.IntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=250, null=True)),
                ('random_id', models.CharField(blank=True, max_length=45, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant_added_by', to='customAuth.user')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_user', to='customAuth.user')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TenantDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('document', models.FileField(upload_to='tenant')),
                ('created_at', models.CharField(blank=True, default='none', max_length=35, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant_document_added_by', to='customAuth.user')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='LeaseTermination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('reason', models.CharField(default='End of lease term', max_length=35)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='termination_added_by', to='customAuth.user')),
                ('lease', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.lease')),
            ],
        ),
        migrations.AddField(
            model_name='lease',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_lease', to='tenant.tenant'),
        ),
        migrations.AddField(
            model_name='lease',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_lease', to='property.unit'),
        ),
        migrations.CreateModel(
            name='Guarantors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('calling_code', models.PositiveIntegerField(default=254)),
                ('relationship_type', models.CharField(default='family', max_length=35)),
                ('relationship', models.CharField(blank=True, max_length=55, null=True)),
                ('has_accepted', models.CharField(default='Not yet', max_length=15)),
                ('notes', models.TextField(blank=True, max_length=500, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guarator_added_by', to='customAuth.user')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.BigIntegerField()),
                ('calling_code', models.PositiveIntegerField(default=254)),
                ('relationship_type', models.CharField(default='family', max_length=35)),
                ('relationship', models.CharField(blank=True, max_length=55, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='emergency_added_by', to='customAuth.user')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
    ]