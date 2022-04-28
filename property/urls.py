from django.urls import path
from . import views
app_name = "property"


urlpatterns = [
    path('', views.dashboard.as_view(), name="dashboard-empty"),
    path('dashboard/', views.dashboard.as_view(), name="dashboard"),
    path('property/', views.property.as_view(), name="property"),
    path('units/', views.units.as_view(), name="units"),



    path('construction/', views.construction.as_view(), name="construction"),
   
    path('unit-detail/<int:unit>/', views.unit_detail.as_view(), name="unit-detail"),
    path('unit-detail2/<int:unit>/', views.unit_detail2.as_view(), name="unit-detail2"),
    path('units/<int:property>/', views.units.as_view(), name="units"),
    path('update_units/', views.unit_update, name="update-units"),
    path('prepare/', views.prepare_unit, name="prepare-unit"),
    
    
    path('property/<int:property>/', views.property_detail.as_view(), name="details"),
    path('property-rud/<int:id>/', views.EditDelete_property.as_view(), name='property-rud'),
    path('property-listcreate/', views.ListCreate_property.as_view(), name='property-listcreate'),
    path('documents-listcreate/', views.ListCreate_documents.as_view(), name='documents-listcreate'),
    path('documents-rud/<int:id>/', views.EditDelete_documents.as_view(), name='documents-rud'),
    path('utility-listcreate/', views.ListCreate_utility.as_view(), name='utility-listcreate'),
    path('utility-rud/<int:id>/', views.EditDelete_utility.as_view(), name='utility-rud'),
    
    path('units-rud/<int:id>/', views.EditDelete_units.as_view(), name='units-rud'),
    path('units-listcreate/', views.ListCreate_units.as_view(), name='units-listcreate'),


    path('features-listcreate/', views.ListCreate_features.as_view(), name='features-listcreate'),
    path('features-rud/<int:id>/', views.EditDelete_features.as_view(), name='features-rud'),

    path('photos-listcreate/', views.ListCreate_photos.as_view(), name='photos-listcreate'),
    path('photos-rud/<int:id>/', views.EditDelete_photos.as_view(), name='photos-rud'),







    
    # path('articles/<int:id>/',views.SalesListView.as_view(),name="list"),
    # path('sales/',views.SalesListView.as_view(),name="list"),
    # path('sales/<pk>',views.SalesDetilView.as_view(),name="detail"),
    # path('csv/',views.UploadTemplateView.as_view(),name="csv"),
    # path('upload/', views.csv_upload_view, name='upload'),

]
