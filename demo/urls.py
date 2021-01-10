'''
Created on 2020年12月11日

@author: Administrator
'''
from django.urls.conf import path
from . import views

app_name = 'demo'

urlpatterns = [
        path('index_demo/', views.index_demo, name='index_demo'),

    ]