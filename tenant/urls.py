from django.urls import path
from . import views
app_name = "tenant"


urlpatterns = [
    # path('', views.dashboard, name="dashboard"),
    path('',views.tenants.as_view(),name="tenants"),
    path('buyers/',views.buyers.as_view(),name="buyers"),
    path("details/<int:id>/", views.details.as_view(),name="details"),
    path("tenant-rud/<int:id>/", views.EditDelete_tenant.as_view(),name="tenant-rud"),
    path("tenant-rud/", views.EditDelete_tenant.as_view(),name="tenant-rud"),
    path('tenant-listcreate/', views.ListCreate_tenant.as_view(), name='tenant-listcreate'),
    
    path("guarantor-rud/<int:id>/", views.EditDelete_guarantor.as_view(),name="guarantor-rud"),
    path("guarantor-rud/", views.EditDelete_guarantor.as_view(),name="guarantor-rud"),
    path('guarantor-listcreate/', views.ListCreate_guarantor.as_view(), name='guarantor-listcreate'),

    path("emergency-rud/<int:id>/", views.EditDelete_emergency.as_view(),name="emergency-rud"),
    path("emergency-rud/", views.EditDelete_emergency.as_view(),name="emergency-rud"),
    path('emergency-listcreate/', views.ListCreate_emergency.as_view(), name='emergency-listcreate'),

    path("documents-rud/<int:id>/", views.EditDelete_documents.as_view(),name="documents-rud"),
    path("documents-rud/", views.EditDelete_documents.as_view(),name="documents-rud"),
    path('documents-listcreate/', views.ListCreate_documents.as_view(), name='documents-listcreate'),
    path('terminate/',views.terminate.as_view(),name="terminate"),
    path("terminate-rud/<int:id>/", views.EditDelete_terminate.as_view(),name="terminate-rud"),
    path("terminate-rud/", views.EditDelete_terminate.as_view(),name="terminate-rud"),
    path('terminate-listcreate/', views.ListCreate_terminate.as_view(), name='terminate-listcreate'),
    
   
    path('lease/',views.lease.as_view(),name="lease"),
    path('purchase/',views.purchase.as_view(),name="purchase"),
    path('test/',views.test_this,name="test"),
    path('lease/<int:id>/',views.lease_details.as_view(),name="lease_details"),
    
     path("lease-rud/<int:id>/", views.EditDelete_lease.as_view(),name="lease-rud"),
    path("lease-rud/", views.EditDelete_lease.as_view(),name="lease-rud"),
    path('lease-listcreate/', views.ListCreate_lease.as_view(), name='lease-listcreate'),
    # path('units/', views.units, name="units"),
    # path('articles/<int:id>/',views.SalesListView.as_view(),name="list"),
    # path('sales/',views.SalesListView.as_view(),name="list"),
    # path('sales/<pk>',views.SalesDetilView.as_view(),name="detail"),
    # path('csv/',views.UploadTemplateView.as_view(),name="csv"),
    # path('upload/', views.csv_upload_view, name='upload'),

]
