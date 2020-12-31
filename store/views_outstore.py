from django.shortcuts import render
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
        if store.__len__()==0:
            return JsonResponse({'status':500, 'msg':'库存未找到，请刷新或查证后再出库！'})
        data['store']=store[0]
        outNo = outstore_form.cleaned_data.get('outNo')
        outStore = OutStore.objects.filter(outNo=outNo)
        if outStore:
            return JsonResponse({'status':500, 'msg':'该采购单已入库！不能重复入库'})
        OutStore.objects.create(**data)
        return JsonResponse({'status':200, 'msg':'新增成功'})
    return JsonResponse({'status': 500, 'msg':outstore_form._errors})

def outstore_query(request):
    return

def outstore_lists(request):
    outstore_form = OutStoreForm()
    outstores = OutStore.objects.all()
    return render(request, 'store/outstore_lists.html', locals())