import datetime

from django.shortcuts import render

from project.models import Project
from store.forms import OutStoreForm, InStoreForm
from store.models import OutStore, Store
from django.http.response import JsonResponse


# Create your views here.
def outstore_save(request):
    outstore_form = OutStoreForm(request.POST)
    if outstore_form.is_valid():
        data = outstore_form.cleaned_data
        data.pop('mtype')
        data.pop('mclass')
        data.pop('mname')
        data.pop('specifi')
        data.pop('pname')
        data.pop('unit')
        # 生成出库单号outNo = C + 年月日 + 四位序号
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        outs = OutStore.objects.values('outNo').filter(date=now_date).order_by('-create_time')
        if outs:
            data['outNo'] = 'C%d' % (int(outs[0]['outNo'][1:]) + 1)
        else:
            data['outNo'] = 'C' + now_date.replace('-', '') + '0001'

        # 判定库存是否存在，并关联项目
        storeid = outstore_form.cleaned_data.get('store')
        store = Store.objects.filter(id=storeid)
        if store.__len__() == 0:
            return JsonResponse({'status': 500, 'msg': '库存未找到，请刷新或查证后再出库！'})
        if store[0].num < float(data['num']):  # 判定库存数量是否满足出库要求
            return JsonResponse({'status': 500, 'msg': '库存剩余：%s，不满足出库要求，请调整出库数量再出库！' % store[0].num})
        data['store'] = store[0]
        data['price'] = store[0].price

        OutStore.objects.create(**data)
        return JsonResponse({'status': 200, 'msg': '出库成功！'})
    return JsonResponse({'status': 500, 'msg': outstore_form.errors})


def out_store_query(request):
    out_No = request.POST.get('out_No')
    m_name = request.POST.get('m_name')
    m_type = request.POST.get('m_type')
    m_class = request.POST.get('m_class')
    reciTeam = request.POST.get('reciTeam')
    searchCondition = dict()
    m_searchCondition = dict()
    outs = []
    re_data = []
    if out_No:
        searchCondition['outNo'] = out_No
    if m_name:
        m_searchCondition['mname__contains'] = m_name
    if m_type:
        m_searchCondition['mtype__contains'] = m_type
    if m_class:
        m_searchCondition['mclass__contains'] = m_class
    if reciTeam:
        searchCondition['reciTeam__contains'] = reciTeam
    if m_searchCondition:
        m_list = Store.objects.values('id').filter(**m_searchCondition)
        if m_list:
            searchCondition['store_id__in'] = m_list
        else:
            return JsonResponse(re_data, safe=False)

    outs = OutStore.objects.values().filter(**searchCondition)
    out_data = list(outs)
    if outs:
        for d in out_data:
            s_objs = Store.objects.values().filter(id=d['store_id'])
            p = Project.objects.values().filter(id=s_objs[0]['project_id'])
            s_list = list(s_objs)[0]
            s_list['project'] = list(p)[0]
            s_list['mtype_mclass'] = s_list['mtype'] + ' > ' + s_list['mclass']
            d['store'] = s_list
            re_data.append(d)
    else:
        return JsonResponse(out_data, safe=False)
    return JsonResponse(re_data, safe=False)


def outstore_lists(request):
    store_form = InStoreForm()
    return render(request, 'store/outstore_lists.html', locals())


# 删除材料出库记录
def outstore_del(request):
    try:
        ids = request.POST.get('id')
        OutStore.objects.filter(id=ids).delete()
        return JsonResponse({'status': 200, 'msg': '删除成功！'})
    except Exception as e:
        return JsonResponse({'status': 500, 'msg': '删除失败'})
