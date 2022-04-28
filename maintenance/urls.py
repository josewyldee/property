from django.urls import path
from . import views
app_name = "maintenance"


urlpatterns = [
    path('',views.index.as_view(),name="index"),
    path('<int:maintenance>/', views.details.as_view(), name="details"),

    path("maintenance-rud/<int:id>/", views.EditDelete_maintenance.as_view(),name="maintenance-rud"),
    path("maintenance-rud/", views.EditDelete_maintenance.as_view(),name="maintenance-rud"),
    path('maintenance-listcreate/', views.ListCreate_maintenance.as_view(), name='maintenance-listcreate'),

    path("cost-rud/<int:id>/", views.EditDelete_cost.as_view(),name="cost-rud"),
    path("cost-rud/", views.EditDelete_cost.as_view(),name="cost-rud"),
    path('cost-listcreate/', views.ListCreate_cost.as_view(), name='cost-listcreate'),

    path("document-rud/<int:id>/", views.EditDelete_document.as_view(),name="document-rud"),
    path("document-rud/", views.EditDelete_document.as_view(),name="document-rud"),
    path('document-listcreate/', views.ListCreate_document.as_view(), name='document-listcreate'),
    
    # path('maintenance_summary/', views.maintenance_summary.as_view(), name="maintenance_summary"),
    # path('maintenance_summary_table/', views.maintenance_summary_table, name="maintenance_summary_table"),

]
