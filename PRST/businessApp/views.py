from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect

from userApp.models import Employee, Administrator,CommissionedEmployee
from constants import INVALID_KIND


def get_user(request, kind):
    if request.session.get('kind', '') != kind or kind not in ["Employee", "Administrator"]:
        return None

    uid = request.session.get('user', '')
    if kind == "Employee":
        Employee_set = Employee.objects.filter(id=uid)
        if Employee_set.count() == 0:
            return None
        else:
            try:
                user = CommissionedEmployee.objects.get(id=uid)
            except CommissionedEmployee.DoesNotExist:
                try:
                    user = Employee.objects.get(id=uid)
                except Employee.DoesNotExist:
                    user = None
        return user
    else:
        Administrator_set = Administrator.objects.filter(id=uid)
        if Administrator_set.count() == 0:
            return None
        else:
            return Administrator_set[0]

def home(request, kind):
    if kind == "Employee":
        return employee_home(request)
    elif kind == "Administrator":
        return administrator_home(request)
    return HttpResponse(INVALID_KIND)


def employee_home(request):
    kind = "Employee"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)
    
    info = {
        "name": user.username,
        "kind": kind,
        "user": user,
    }

    context = {
        "info": info,
    }
    print(info)
    print(info["user"].is_commissioned())
    return render(request, 'business/nav.html', context)

def administrator_home(request):
    kind = "Administrator"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)
    
    info = {
        "name": user.username,
        "kind": kind,
    }

    context = {
        "info": info,
    }
    return render(request, 'business/nav.html', context)