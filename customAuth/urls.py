from django.urls import path
from . import views
app_name = "customAuth"


urlpatterns = [
    # path('', views.dashboard.as_view(), name="dashboard"),
    path('admin/', views.admin.as_view(), name='admin'),
    path("profile/<int:id>/", views.profile.as_view(),name="profile"),
    path("admin-rud/<int:id>/", views.EditDelete_admin_profile.as_view(),name="admin-rud"),
    path('admin-listcreate/', views.ListCreate_admin_profile.as_view(), name='admin-listcreate'),

    path('employee/', views.employee.as_view(), name='employee'),
    path("employee-rud/<int:id>/", views.EditDelete_employee_profile.as_view(),name="employee-rud"),
    path('employee-listcreate/', views.ListCreate_employee_profile.as_view(), name='employee-listcreate'),

    path('tenant/', views.tenant.as_view(), name='tenant'),
    path("tenant-rud/<int:id>/", views.EditDelete_tenant_profile.as_view(),name="tenant-rud"),
    path('tenant-listcreate/', views.ListCreate_tenant_profile.as_view(), name='tenant-listcreate'),
]
