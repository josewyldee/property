from django.contrib import admin
from .models import Charges,Invoice,Receipt,Late_fee_types,Statement,Expense

@admin.register(Charges)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','amount','duration')
    list_filter=('name','amount','duration')
    search_fields=['name','amount','duration']
@admin.register(Statement)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','statement_invoice','statement_receipt','amount','amount_sorted','lease','created_on')
    list_filter=('lease','type')
@admin.register(Invoice)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','name','amount','amount_sorted','invoice_group','lease','is_cancelled')
    list_filter=('is_cancelled','lease','invoice_type')
    search_fields=['name','amount','invoice_type']

@admin.register(Receipt)
class PostAdmin(admin.ModelAdmin):
    list_display=('amount','receipt_type','receipt_group','lease','invoice')
    list_filter=('is_cancelled','lease','receipt_type')
    search_fields=['amount','receipt_type']
  
@admin.register(Late_fee_types)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','created_for','value')
    list_filter=('name','created_for','value')
    search_fields=('name','created_for','value')

@admin.register(Expense)
class PostAdmin(admin.ModelAdmin):
    list_display=('expense_name','amount','payee')
    list_filter=('expense_name','amount','payee')
    search_fields=('expense_name','amount','payee')

