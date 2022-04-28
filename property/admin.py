from django.contrib import admin
from .models import Property, Property_documents,Unit,Unit_features,Unit_photos, Utility_bills

@admin.register(Property)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','property_name','property_category','property_type','active')
    list_filter=('property_category','property_type')
    search_fields=['property_name','property_category','property_category','property_type']
    list_editable = ['property_name','property_category']

    # prepopulated_fields = {"slug": ("title",)}
    
@admin.register(Unit)
class PostAdmin(admin.ModelAdmin):
    list_display=('unit_property','unit_name','unit_charges','unit_features','unit_photos','id')
    list_filter=('unit_name','unit_category','unit_type','occupancy_status')
    search_fields=['unit_name','unit_category','unit_type','occupancy_status']
@admin.register(Unit_features)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','id')
    search_fields=['name']
@admin.register(Unit_photos)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','id')
    search_fields=['name']
@admin.register(Property_documents)
class PostAdmin(admin.ModelAdmin):
    list_display=('name','id','category')
    search_fields=['name']
@admin.register(Utility_bills)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','name','amount',"month_date","year_date")
    search_fields=['name']


