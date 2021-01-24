from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [
    path('totals/', views.totals_report, name='totals'),
    path('team/', views.team_details_report, name='team')
]
