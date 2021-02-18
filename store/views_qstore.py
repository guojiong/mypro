'''
Created on 2020年12月25日

@author: Administrator
'''
from django.db import utils, models
from django.db.models import Sum, F

from store.forms import OutStoreForm
from store.models import Store, InStore, OutStore
from django.shortcuts import render
from django.http.response import JsonResponse
from project.models import Project


def qstore_lists(request):
    store_form = OutStoreForm()
    # stores = Store.objects.all()
    return render(request, 'store/qstore_lists.html', locals())


def qstore_query(request):
    store_id = request.POST.get('id')
    if store_id:
        storeQset = Store.objects.values().filter(id=store_id)
        if storeQset.__len__():
            ret_list = list(storeQset)
            project = Project.objects.get(id=ret_list[0]['project_id'])
            ret_list[0]['pname'] = project.name
            return JsonResponse(ret_list, safe=False)
        else:
            return JsonResponse({'status': 500, 'msg': '查询失败'})
    return JsonResponse({'status': 500, 'msg': '未获取到查询条件'})


def q_store_data(request):
    m_type = request.POST.get('m_type')
    m_class = request.POST.get('m_class')
    m_name = request.POST.get('m_name')
    re_list = []
    searchCondition = {}
    if m_type:
        searchCondition['mtype__contains'] = m_type
    if m_class:
        searchCondition['mclass__contains'] = m_class
    if m_name:
        searchCondition['mname__contains'] = m_name

    tmp = Store.objects.values().filter(**searchCondition)
    if tmp:
        for s in tmp:
            p = Project.objects.values().filter(id=s['project_id'])
            s['project'] = list(p)[0]
            i = InStore.objects.values('num', 'materialfee').filter(store=s['id']).aggregate(Sum('num'), Sum('materialfee'))
            s['iNum'] = i['num__sum']
            s['iMaterialfee'] = i['materialfee__sum']

            # o = OutStore.objects.values('num', 'price').filter(store=s['id']).aggregate(Sum('num'), Sum('price'))
            o = OutStore.objects.values('num').filter(store=s['id']).annotate(
                all_cost=Sum(F('num') * F('price'), output_field=models.FloatField()))
            if o:
                s['oNum'] = o[0]['num']
                s['oMaterialfee'] = o[0]['all_cost']
            else:
                s['oNum'] = ''
                s['oMaterialfee'] = ''

            re_list.append(s)

    return JsonResponse(re_list, safe=False)


def q_in_store_by_store_id(request):
    store_ids = request.POST.get('id')
    re_list = []
    if store_ids:
        s = Store.objects.filter(id=store_ids)
        in_store = InStore.objects.values().filter(project=s[0].project, mtype=s[0].mtype, mclass=s[0].mclass, mname=s[0].mname, specifi=s[0].specifi)
        if in_store:
            for tmp in in_store:
                project = Project.objects.values().filter(id=tmp['project_id'])
                tmp['project'] = project[0]
                re_list.append(tmp)
    return JsonResponse(re_list, safe=False)
