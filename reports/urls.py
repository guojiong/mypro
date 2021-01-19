from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [
    path('data/', views.totals_report, name='t_data'),
    path('', views.totals_page, name='totals')
]
