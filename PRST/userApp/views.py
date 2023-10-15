from django.shortcuts import render

from django.http.response import HttpResponse

from constants import INVALID_KIND
from userApp.forms import EmpLoginFrom, AdminLoginFrom

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
            uid = form.cleaned_data["uid"]

            temp_res = "hello, %s" % uid
            return HttpResponse(temp_res)
        else:
            context['form'] = form
    else:
        if kind == "Administrator":
            form = AdminLoginFrom()
        else:
            form = EmpLoginFrom()

        context['form'] = form

    return render(request, 'user/login_detail.html', context)

def home(request):
    return render(request, 'user/login_home.html')