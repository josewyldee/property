from django.urls import path
from . import views

app_name = 'searchdata'

urlpatterns = [
    path('units/', views.units, name='units'),
    path('tenants/', views.tenants, name='tenants'),
    path('tenants_lease/', views.tenants_lease, name='tenants_lease'),
    path('buyers/', views.buyers, name='buyers'),
    path('tenants-account/', views.tenants_account, name='tenants-account'),
    path('invoice-property/', views.create_invoice_property, name='invoice-property'),
    path('invoice-unit/', views.create_invoice_unit, name='invoice-unit'),
    path('communications-emails/', views.select_tenants_email, name='communications-emails'),
    path('invoice-late_fee_types/', views.late_fee_types, name='invoice-late_fee_types'),
    path('admin/', views.admin, name='admin'),
    path('select_units/', views.select_units, name='select_units'),
    path('select_property/', views.select_property, name='select_property'),
    path('select_invoice/', views.select_invoice, name='select_invoice'),
    path('select_payment/', views.select_payment, name='select_payment'),
    path('property_units/', views.property_units, name='property_units'),
    path('payees/', views.payees, name='payees'),
    path('unit_maintenance/', views.unit_maintenance, name='unit_maintenance'),
    path('lease/', views.lease, name='lease'),
]

