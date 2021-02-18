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
        path('in_data/', views.in_store_data, name='in_data'),
        path('in_del/', views.instore_del, name='in_del'),

    #   库存
        path('qlists/', views_qstore.qstore_lists, name='qlists'),
        path('qstore/', views_qstore.qstore_query, name='qstore'),
        path('store_data/', views_qstore.q_store_data, name='store_data'),
        path('q_store_by_ids/', views_qstore.q_in_store_by_store_id, name='q_store_by_ids'),

    #   出库单
        path('out_lists/', views_outstore.outstore_lists, name='out_lists'),
        path('outsave/', views_outstore.outstore_save, name='outsave'),
        path('out_data/', views_outstore.out_store_query, name='out_data'),
        path('out_del/', views_outstore.outstore_del, name='out_del'),
    ]