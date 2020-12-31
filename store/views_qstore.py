'''
Created on 2020年12月25日

@author: Administrator
'''
from store.forms import OutStoreForm
from store.models import Store
from django.shortcuts import render
from django.http.response import JsonResponse
from project.models import Project

def qstore_lists(request):
    store_form = OutStoreForm()
    stores = Store.objects.all()
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
            return JsonResponse({'status':500, 'msg':'查询失败'})
    return JsonResponse({'status':500, 'msg':'未获取到查询条件'})

