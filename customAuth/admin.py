from django.contrib import admin
from .models import User,AdminProfile,Payee
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    list_display = ['email', 'is_syestem_admin','is_tenant','first_name','pk']
    list_filter = ['is_syestem_admin','is_tenant']
    fieldsets = (
        (None, {'fields': ('email', 'password','username')}),
        # ('Personal info', {'fields': ('first_name','last_name')}),
        ('Permissions', {'fields': ('is_superuser','is_staff')}),
        ('Notifications', {'fields': ('notifications',)}),
        ('user type', {'fields': ('is_syestem_admin', 'is_tenant', 'is_employee','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','last_name')}
        ),
    )
  
    search_fields = ['email','first_name','last_name']
    ordering = ['email','first_name','last_name']
    filter_horizontal = ()
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    # list_filter = ['user.is_syestem_admin','user.is_tenant']
    fieldsets = (
        (None, {'fields': ('user', 'name','image')}),
      
    )
 
    search_fields = ['user','name']
    ordering = ['name']
    filter_horizontal = ()
admin.site.register(AdminProfile, ProfileAdmin)


@admin.register(Payee)
class PostAdmin(admin.ModelAdmin):
    data=('name','category','payee_category')
    list_display=data
    list_filter=data
    search_fields=data