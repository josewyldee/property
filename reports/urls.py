from django.urls import path
from . import views
app_name = "reports"


urlpatterns = [

    path('income_summary/', views.income_summary.as_view(), name="income_summary"),
    path('income_summary_table/', views.income_summary_table, name="income_summary_table"),
    path('statements/', views.statements.as_view(), name="statements"),

    path('occupancy/', views.occupancy.as_view(), name="occupancy"),
    path('occupancy_table/', views.occupancy_table, name="occupancy_table"),

    path('maintenance_summary/', views.maintenance_summary.as_view(), name="maintenance_summary"),
    path('maintenance_summary_table/', views.maintenance_summary_table, name="maintenance_summary_table"),

    path('percentage_earnings/', views.percentage_earnings.as_view(), name="percentage_earnings"),
    path('percentage_earnings_table/', views.percentage_earnings_table, name="percentage_earnings_table"),
   

]
