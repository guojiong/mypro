from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.totals_report, name='totals')
]
