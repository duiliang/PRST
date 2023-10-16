from django.shortcuts import render
from django.http.response import HttpResponse

from constants import INVALID_KIND
from userApp.forms import EmpLoginForm, AdminLoginForm
from userApp.cbvs import CreateEmployeeView, CreateAdminView

def login(request, *args, **kwargs):
    if not kwargs or kwargs.get("kind", "") not in ["Employee", "Administrator"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]
    context = {'kind': kind}

    if request.method == 'POST':
        if kind == "Employee":
            form = EmpLoginForm(data=request.POST) 
        else:
            form = AdminLoginForm(data=request.POST)

        if form.is_valid():
            id = form.cleaned_data["id"]

            temp_res = "hello, %s" % id
            return HttpResponse(temp_res)
        else:
            context['form'] = form
    elif request.method == 'GET':
        if request.GET.get('id'):
            context['id'] = request.GET['id']
            data = {'id': request.GET['id']}
            if kind == "Employee":
                form = EmpLoginForm(data)
            else:
                form = AdminLoginForm(data)
        else:
            if kind == "Employee":
                form = EmpLoginForm()
            else:
                form = AdminLoginForm()
        
        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get['from_url']

    return render(request, 'user/login_detail.html', context)

def home(request):
    return render(request, 'user/login_home.html')

def register(request, kind):
    func = None
    if kind == "Employee":
        func = CreateEmployeeView.as_view()
    elif kind == "Administrator":
        func = CreateAdminView.as_view()


    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)