from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from iia.registry import apps_registry
from django.apps import apps
from iia.plugins import data

def home(request):
    return render(request, 'home.html', {'apps': apps_registry})

def home_logo(request):
    with open('./templates/favicon.ico', 'rb') as f:
        return HttpResponse(f.read(), content_type='image/x-icon')

def home_res(request, file):
    print(file)
    return render(request, f'resources/{file}')

def app_home(request, app_name):
    # try:
    # 根据 app_name 确定要加载的模板文件路径
    template_name = f'{app_name}/main.html'
    print("Load HTML",template_name)
    return render(request, template_name, {'data':data[app_name]})
    # except Exception:
    #     return render(request, 'error.html', {'message': 'Template not found'})

def app_function(request, app_name, app_function):
    # try:
    # 根据 app_name 确定要加载的模板文件路径
    function = getattr(data[app_name],app_function,None)
    if function is not None:
        return JsonResponse({'res':function(**dict(request.GET))})
    # template_name = f'{app_name}/main.html'
    # return render(request, template_name, {'data':data[app_name]})
    # except Exception:
    #     return render(request, 'error.html', {'message': 'Function not found'})
