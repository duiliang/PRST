from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.urls import reverse

from constants import INVALID_KIND
from userApp.forms import EmpLoginForm, AdminLoginForm
from userApp.cbvs import CreateEmployeeView, CreateAdminView,DetailAdminView,DetailEmpView
from userApp.models import Employee, Administrator
def login(request, kind):
    if kind not in ["Employee", "Administrator"]:
        return HttpResponse(INVALID_KIND)

    if request.method == 'POST':
        if kind == "Employee":
            form = EmpLoginForm(data=request.POST) 
        else:
            form = AdminLoginForm(data=request.POST)

        if form.is_valid():
            id = form.cleaned_data["id"]
            if kind == "Employee":
                object_set = Employee.objects.filter(id=id)
            else:
                object_set = Administrator.objects.filter(id=id)
            if object_set.count() == 0:
                form.add_error('id', '不存在的ID')
            else:
                user = object_set[0]
                if form.cleaned_data["password"] != user.password:
                    form.add_error('password', '密码错误')
                else:
                    request.session['kind'] = kind
                    request.session['user'] = id
                    request.session['id'] = user.id

                    return redirect("business", kind=kind)
        return render(request, 'user/login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {"kind": kind}
        if request.GET.get("id"):
            id = request.GET.get("id")
            context["id"] = id
            if kind == "Employee":
                form = EmpLoginForm(initial={"id": id})
            else:
                form = AdminLoginForm(initial={"id": id})
        else:
            if kind == "Employee":
                form = EmpLoginForm()
            else:
                form = AdminLoginForm()
        context["form"] = form
        if request.GET.get("from"):
            context["from"] = request.GET.get("from")
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

def logout(request):
    if request.session.get('kind', ''):
        del request.session['kind']
    if request.session.get('user', ''):
        del request.session['user']
    if request.session.get('id', ''):
        del request.session['id']
    return redirect(reverse("login"))


def show(request,kind):
    func=None
    if kind == "Employee":
        func = DetailEmpView.as_view()
    elif kind == "Administrator":
        func = DetailAdminView.as_view()
    else:
        return HttpResponse(INVALID_KIND)
    
    pk = request.session.get('id')
    if pk:
        context = {
            "name" :request.session.get('name',""),
            "kind":request.session.get('kind',""),
        }
        print(context)
        return func(request,pk=pk,context=context)
    return redirect(reverse("login"))