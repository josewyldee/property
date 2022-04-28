from django.contrib import admin
from.models import Maintenance,Cost,Document
# Register your models here.
@admin.register(Maintenance)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','status','priority')
    list_filter=('name','status','priority')
    search_fields=['name','status','priority']
    
@admin.register(Cost)
class PostAdmin(admin.ModelAdmin):
    list_display=('cost_type','cost_name','cost_total')
    list_filter=('cost_type','cost_name','cost_total')
    search_fields=['cost_type','cost_name','cost_total']
@admin.register(Document)
class PostAdmin(admin.ModelAdmin):
    list_display=('name',)
    list_filter=('name',)
    search_fields=['name']