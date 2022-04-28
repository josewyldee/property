from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('property.urls', namespace="property2")),
    path('property/', include('property.urls', namespace="property")),
    path('tenants/', include('tenant.urls', namespace="tenant")),
    path('maintenance/', include('maintenance.urls', namespace="maintenance")),
    path('finance/', include('finance.urls', namespace="finance")),
    path('communications/', include('communications.urls', namespace="communications")),
    path('select/', include('searchdata.urls')),
    path('tenant_dashboard/', include('tenant_dashboard.urls')),
     path('accounts/', include('allauth.urls')),
     path('customAuth/', include('customAuth.urls')),
     path('notifications/', include('notifications.urls')),
     path('chat/', include('chat.urls')),
     path('reports/', include('reports.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)