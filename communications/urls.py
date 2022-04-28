from django.urls import path
from . import views
app_name = "communications"


urlpatterns = [
    path('send_email/', views.send_email, name="send_email"),
    path('email/', views.email.as_view(), name="email"),
    path('email-listcreate/', views.ListCreate_emails.as_view(), name='email-listcreate'),
    path('email-rud/<int:id>/', views.EditDelete_emails.as_view(), name='email-rud'),


    path('test/',views.test,name="test"),


]
