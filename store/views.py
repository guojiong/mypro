from django.shortcuts import render
from store.forms import InStoreForm, OutStoreForm
from store.models import InStore, OutStore, Store
from django.http.response import JsonResponse
from project.models import Project

# Create your views here.
def instore_lists(request):
    store_form = InStoreForm()
    # stores = InStore.objects.all()
    return render(request, 'store/instore_lists.html', locals())

def instore_save(request):
    instore_form = InStoreForm(request.POST)
    if instore_form.is_valid():
        data = instore_form.cleaned_data
        ids = instore_form.cleaned_data.get('id')
        receiptNo = instore_form.cleaned_data.get('receiptNo')
        project=instore_form.cleaned_data.get('project');
        projectobj = Project.objects.filter(name=project)
        if projectobj.__len__()==0:
            return JsonResponse({'status':500, 'msg':'所属项目不存在' })
        data['project'] = projectobj[0]
        if ids:
            InStore.objects.filter(id=ids).update(**data)
            return JsonResponse({'status':200, 'msg':'更新成功'})
        else:
            store = InStore.objects.filter(receiptNo=receiptNo)
            if store:
                return JsonResponse({'status':500, 'msg':'该采购单已入库！不能重复入库'})
            InStore.objects.create(**data)
            return JsonResponse({'status':200, 'msg':'新增成功'})
    return JsonResponse({'status': 500, 'msg':instore_form._errors})


def store_query(request):
    project_id = request.POST.get()
    m_type = request.POST.get()
    m_class = request.POST.get()
    m_name = request.POST.get()
    m_specifi = request.POST.get()
    searchCondition = {}
    if project_id:
        searchCondition[''] = project_id
    if m_type:
        searchCondition['m'] = m_type
    if m_class:
        searchCondition[''] = m_class
    if m_name:
        searchCondition[''] = m_name
    if m_specifi:
        searchCondition[''] = m_specifi
    tmp = InStore.objects.values().filter(**searchCondition)
    tmp = InStore.objects.filter()

    return


def in_store_data(request):
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

    tmp = InStore.objects.values().filter(**searchCondition)

    if tmp:
        for in_store in tmp:
            p = Project.objects.values().filter(id=in_store['project_id'])
            in_store['project'] = p[0]
            re_list.append(in_store)

    return JsonResponse(re_list, safe=False)
