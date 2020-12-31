'''
Created on 2020年12月11日

@author: Administrator
'''
from django.urls.conf import path
from store import views, views_qstore, views_outstore
app_name = 'store'

urlpatterns = [
    #   入库单
        path('inlists/', views.instore_lists, name='inlists'),
        path('save/', views.instore_save, name='save'),
    #   库存
        path('qlists/', views_qstore.qstore_lists, name='qlists'),
        path('qstore/', views_qstore.qstore_query, name='qstore'),
    #   出库单
        path('outlists/', views_outstore.outstore_lists, name='outlists'),
        path('outsave/', views_outstore.outstore_save, name='outsave'),
    ]