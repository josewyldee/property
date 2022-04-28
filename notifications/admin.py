from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class PostAdmin(admin.ModelAdmin):
    list_display=('notification_type','from_group','from_user','to_group')
    search_fields=['notification_type']


