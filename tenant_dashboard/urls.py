from django.urls import path
from . import views
app_name = "tenant_dashboard"


urlpatterns = [
    path('', views.dashboard.as_view(), name="dashboard"),
    path('dashboard', views.dashboard.as_view(), name="dashboard"),
    path('maintenance/', views.maintenance.as_view(), name="maintenance"),
    path('profile/', views.profile.as_view(), name="profile"),

    path("maintenance-rud/<int:id>/", views.EditDelete_maintenance.as_view(),name="maintenance-rud"),
    path("maintenance-rud/", views.EditDelete_maintenance.as_view(),name="maintenance-rud"),
    path('maintenance-listcreate/', views.ListCreate_maintenance.as_view(), name='maintenance-listcreate'),

    path("document-rud/<int:id>/", views.EditDelete_document.as_view(),name="document-rud"),
    path("document-rud/", views.EditDelete_document.as_view(),name="document-rud"),
    path('document-listcreate/', views.ListCreate_document.as_view(), name='document-listcreate'),

    path('receipt-pdf/<lease>/<statement>/<receipt>', views.receipt_pdf.as_view(), name='receipt-pdf'),
    path('invoice-pdf/<lease>/<statement>/<invoice>', views.invoice_pdf.as_view(), name='invoice-pdf'),
    # path('',views.tenants.as_view(),name="tenants"),
   

]
