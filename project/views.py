from django.shortcuts import render
from django.http.response import JsonResponse

from store.models import Store, InStore
from .models import Project
from . import forms
from .forms import ProjectForm


# Create your views here.
def index(request):
    return render(request, 'base.html', )


def lists(request):
    project_form = forms.ProjectForm()
    # objprojects = Project.objects
    # projects = objprojects.all()
    return render(request, 'project/project_lists.html', locals())


def project_save(request):
    form_add = ProjectForm(request.POST)
    if form_add.is_valid():
        ids = form_add.cleaned_data.get('id')
        code = form_add.cleaned_data.get('code')
        name = form_add.cleaned_data.get('name')
        remark = form_add.cleaned_data.get('remark')
        data = {
            'code': code,
            'name': name,
            'remark': remark,
            }
        if ids:
            Project.objects.filter(id=ids).update(**data)
            return JsonResponse({'status': '200', 'msg': '更新成功'})
        else:
            project = Project.objects.filter(code=code)
            if project:
                return JsonResponse({'status': '500', 'msg': '项目编号已存在，请重新录入！'})
            Project.objects.create(**data)
            return JsonResponse({'status': '200', 'msg': '新增成功'})
    return JsonResponse({'status': '500', 'msg': form_add._errors})


def project_query(request):
    project_id = request.POST.get('id')
    projects_list = []
    if project_id:
        projects = Project.objects.values().filter(id=project_id)
        projects_list = list(projects)
    return JsonResponse(projects_list, safe=False)


def project_del(request):
    project_id = request.GET.get('id')
    project = Project.objects.filter(id=project_id)
    if project:
        project.update(status=1)  # delete()
    log_project = Project.objects.filter(id=project_id, status=0)
    if log_project:
        return JsonResponse({'status': 500, 'msg': '删除失败'})
    return JsonResponse({'status': 200, 'msg': '删除成功'})


def datatable(request):
    objprojects = Project.objects
    code = request.POST.get('code')
    name = request.POST.get('name')
    projects = ''
    if code:
        projects = objprojects.values().filter(code__contains=code, status=0)
        if name and projects:
            projects = projects.filter(name__contains=name, status=0)
    elif name:
        projects = objprojects.values().filter(name__contains=name, status=0)
    else:
        projects = objprojects.values().filter(status=0)
    projects_list = list(projects)
    return JsonResponse(projects_list, safe=False)


def test(request):
    return render(request, 'test_datatable.html')

