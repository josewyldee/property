from django.urls import path

from . import views

app_name = "notifications"

urlpatterns = [
    path('all/', views.index, name='index'),
    path('open/<int:notification>/<str:notification_type>/<str:id>/', views.open, name='open'),
    # path('<str:room_name>/', views.room, name='room'),

  
    path('notifications-rud/<int:id>/', views.EditDelete_notification.as_view(), name='notifications-rud'),
    path('update_status/<int:id>/', views.update_status, name='update_status'),
    path('notification-listcreate/', views.ListCreate_notification.as_view(), name='notification-listcreate'),
]