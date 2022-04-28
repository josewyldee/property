from django.contrib import admin
from .models import Email

@admin.register(Email)
class PostAdmin(admin.ModelAdmin):
    list_display=('subject','type','lease')
    list_filter=('subject','type','lease')


