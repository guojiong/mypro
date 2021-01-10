from django.shortcuts import render

from project.models import Project
from store.forms import OutStoreForm
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
        storeid = outstore_form.cleaned_data.get('store')
        store = Store.objects.filter(id=storeid)
        if store.__len__() == 0:
            return JsonResponse({'status':500, 'msg':'库存未找到，请刷新或查证后再出库！'})
        data['store']=store[0]
        outNo = outstore_form.cleaned_data.get('outNo')
        outStore = OutStore.objects.filter(outNo=outNo)
        if outStore:
            return JsonResponse({'status':500, 'msg':'该采购单已入库！不能重复入库'})
        OutStore.objects.create(**data)
        return JsonResponse({'status':200, 'msg':'新增成功'})
    return JsonResponse({'status': 500, 'msg':outstore_form._errors})


def out_store_query(request):
    out_No = request.POST.get('out_No')
    m_name = request.POST.get('m_name')
    outs = []
    re_data = []
    if out_No:
        outs = OutStore.objects.values().filter(outNo=out_No)
        if outs and m_name:     # 材料名称不为空， 且存在出库单号
            m_list = Store.objects.values('id').filter(mname__contains=m_name)
            if m_list:          # 根据材料名称查询结果不为空，则根据库存id过滤
                outs = outs.filter(store_id__in=m_list)
            else:               # 否则查询结果为空
                outs = []
    elif m_name:
        m_list = Store.objects.values('id').filter(mname__contains=m_name)
        if m_list:
            outs = OutStore.objects.values().filter(store__in=m_list)
    else:
        outs = OutStore.objects.values().all()
    if outs:
        out_data = list(outs)
        for d in out_data:
            s_objs = Store.objects.values().filter(id=d['store_id'])
            p = Project.objects.values().filter(id=s_objs[0]['project_id'])
            s_list = list(s_objs)[0]
            s_list['project'] = list(p)[0]
            s_list['mtype_mclass']=s_list['mtype'] + ' > ' + s_list['mclass']
            d['store'] = s_list
            re_data.append(d)
    else:
        return JsonResponse(outs, safe=False)
    return JsonResponse(re_data, safe=False)


def outstore_lists(request):
    return render(request, 'store/outstore_lists.html')
