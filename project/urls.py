'''
Created on 2020年12月11日

@author: Administrator
'''
from django.urls.conf import path
from project import views

app_name = 'project'

urlpatterns = [
    path('',views.index, name='index'),
    path('lists/',views.lists, name='lists'),
    path('query/',views.project_query, name='query'),
    path('del/',views.project_del, name='del'),
    path('save/',views.project_save, name='save'),
    path('test/',views.test, name='test'),
    ]