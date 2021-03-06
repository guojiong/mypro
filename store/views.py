import datetime
import json

from django.core import serializers
from django.shortcuts import render

from mclass.models import Mclass
from store.forms import InStoreForm, OutStoreForm
from store.models import InStore, OutStore, Store
from django.http.response import JsonResponse
from project.models import Project


# 返回页面
def instore_lists(request):
    store_form = InStoreForm()
    # stores = InStore.objects.all()
    return render(request, 'store/instore_lists.html', locals())


# 保存数据
def instore_save(request):
    instore_form = InStoreForm(request.POST)
    if instore_form.is_valid():
        data = instore_form.cleaned_data
        ids = instore_form.cleaned_data.get('id')

        # 生成入库单号receiptNo = R + 年月日 + 四位序号
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        ins = InStore.objects.values('receiptNo').filter(date=now_date).order_by('-create_time')
        if ins:
            data['receiptNo'] = 'R%d' % (int(ins[0]['receiptNo'][1:]) + 1)
        else:
            data['receiptNo'] = 'R' + now_date.replace('-', '') + '0001'

        # 判定项目是否存在，并关联项目
        project = instore_form.cleaned_data.get('project')
        projectobj = Project.objects.filter(id=project)
        if projectobj.__len__() == 0:
            return JsonResponse({'status': 500, 'msg': '所属项目不存在'})
        data['project'] = projectobj[0]

        # if ids: 不提供修改
        #     InStore.objects.filter(id=ids).update(**data)
        #     return JsonResponse({'status': 200, 'msg': '更新成功'})
        # else:

        InStore.objects.create(**data)
        store = Store.objects.filter(project=data['project'], mtype=data['mtype'], mclass=data['mclass'],
                                     mname=data['mname'], specifi=data['specifi'], unit=data['unit']).first()
        InStore.objects.filter(receiptNo=data['receiptNo']).update(store=store)
        return JsonResponse({'status': 200, 'msg': '新增成功'})
    # print(instore_form.errors)
    return JsonResponse({'status': 500, 'msg': str(instore_form.errors)})


# 返回查询数据
def in_store_data(request):
    m_type = request.POST.get('m_type')
    m_class = request.POST.get('m_class')
    m_name = request.POST.get('m_name')
    result = {}
    re_list = []
    searchCondition = {}
    if m_type:
        searchCondition['mtype__contains'] = m_type
    if m_class:
        searchCondition['mclass__contains'] = m_class
    if m_name:
        searchCondition['mname__contains'] = m_name

    tmp = InStore.objects.values().filter(**searchCondition)

    if tmp:
        for in_store in tmp:
            p = Project.objects.values().filter(id=in_store['project_id'])
            in_store['project'] = p[0]
            in_store['mtype_mclass'] = in_store['mtype'] + ' > ' + in_store['mclass']
            re_list.append(in_store)
    result = {
        'instores': re_list
    }
    return JsonResponse(result)


def instore_del(request):
    ids = request.POST.get('id')
    InStore.objects.filter(id=ids).delete()
