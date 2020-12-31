'''
Created on 2020年12月11日

@author: Administrator
'''
from django.urls.conf import path
from . import views

app_name = 'mclass'

urlpatterns = [
        path('lists/', views.lists, name='lists'),
        path('save/', views.mclass_save, name='save'),
        path('query/', views.mclass_query, name='query'),
        path('del/', views.mclass_del, name='del'),
    ]