from django.shortcuts import render
from .models import Mclass
from .forms import MclassForm
from django.http.response import JsonResponse


# Create your views here.
def lists(request):
    mclass_form = MclassForm()
    # mclasses = Mclass.objects.all()
    return render(request, 'mclass/mclass_lists.html', locals())


def mclass_save(request):
    form_add = MclassForm(request.POST)
    if form_add.is_valid():
        ids = form_add.cleaned_data.get('id')
        mtype = form_add.cleaned_data.get('mtype')
        mclass = form_add.cleaned_data.get('mclass')
        content = form_add.cleaned_data.get('content')
        remark = form_add.cleaned_data.get('remark')
        data = {
                'id':ids,
                'mtype': mtype,
                'mclass':mclass,
                'content':content,
                'remark':remark,
            }
        if ids:
            Mclass.objects.filter(id=ids).update(**data)
            return JsonResponse({'status': 200, 'msg': '更新成功'})
        else:
            mclassobj = Mclass.objects.filter(mtype=mtype, mclass=mclass)
            if mclassobj:
                return JsonResponse({'status':'500', 'msg':'材料分类已存在，请重新录入！'})
            Mclass.objects.create(**data)
            return JsonResponse({'status':'200', 'msg':'新增成功'})
    return JsonResponse({'status':'500', 'msg':form_add._errors})


def mclass_query(request):
    mclass_id = request.POST.get('id')
    mclassJson = []
    if mclass_id:
        mclasses = Mclass.objects.filter(id=mclass_id)
        data = {
            'id':mclasses[0].id,
            'mtype': mclasses[0].mtype,
            'mclass': mclasses[0].mclass,
            'content': mclasses[0].content,
            'remark': mclasses[0].remark,
        }
        mclassJson.append(data)
    return JsonResponse(mclassJson, safe=False)


def m_class_data(request):
    obj_m_class = Mclass.objects
    m_type = request.POST.get('m_type')
    m_class = request.POST.get('m_class')
    m_classes = []
    if m_type:
        m_classes = obj_m_class.values().filter(mtype=m_type)
        if m_class and m_classes:
            m_classes = m_classes.filter(mclass__contains=m_class)
    elif m_class:
        m_classes = obj_m_class.values().filter(mclass__contains=m_class)
    else:
        m_classes = obj_m_class.values().all()
    m_classes_list = list(m_classes)
    return JsonResponse(m_classes_list, safe=False)


def m_class_del(request):
    mclass_id = request.GET.get('id')
    mclass = Mclass.objects.filter(id=mclass_id)
    if mclass:
        mclass.delete()
    logmclass = Mclass.objects.filter(id=mclass_id)
    if logmclass:
        return JsonResponse({'status': 500, 'msg': '删除失败'})
    return JsonResponse({'status': 200, 'msg': '删除成功'})
