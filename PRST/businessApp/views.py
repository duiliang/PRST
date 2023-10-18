from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.db.models import Q
from datetime import datetime, timedelta, date
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from userApp.models import Employee, Administrator,CommissionedEmployee
from businessApp.models import TimeCard, PurchaseOrder
from constants import INVALID_KIND, INVALID_REQUEST_METHOD
from businessApp.forms import CreateTimecardForm,CreatePurchaseOrderForm,UpdatePurchaseOrderForm


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
# timecard
def create_timecard(request):
    user = get_user(request, "Employee")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    
    info = {
        "name": user.username,
        "kind": "Employee",
        "user": user,
    }

    if request.method == 'POST':
        form = CreateTimecardForm(data=request.POST)
        form.employee = user
        if form.is_valid():
            timecard = form.save(commit=False)
            timecard.employee = Employee.objects.get(id=user.id)
            if timecard.end_time <= timecard.start_time:
                form.add_error('end_time', '结束时间必须在开始时间之后')
                return render(request, 'business/create_timecard.html', {"form": form, "info": info})
            if user.hour_limit is not None:
                if timecard.end_time.hour - timecard.start_time.hour > user.hour_limit:
                    form.add_error('end_time', '工作时间不能超过最大工作时间')
                    return render(request, 'business/create_timecard.html', {"form": form, "info": info})
            if TimeCard.objects.filter(employee=user, work_date=timecard.work_date).count() > 0:
                form.add_error('work_date', '该日期已存在时间卡')
                return render(request, 'business/create_timecard.html', {"form": form, "info": info})
            delta = datetime.combine(date.min, timecard.end_time) - datetime.combine(date.min, timecard.start_time)
            timecard.work_time = delta.seconds / 3600
            timecard.save()
            return redirect(reverse("timecard_home"))
    elif request.method == 'GET':
        form = CreateTimecardForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)
    return render(request, 'business/create_timecard.html', {"form": form, "info": info})
def timecard_home(request):
    user = get_user(request, "Employee")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    info = {
        "name": user.username,
        "kind": "Employee",
        "user": user,
    }
    q = Q(employee=user)
    context = {
        "info": info,
    }
    context["search_key"] = ""
    context["timecard_list"] = TimeCard.objects.filter(q).order_by('work_date')
    return render(request, 'business/timecard.html', context)

#purchase order
def create_purchaseorder(request):
    user = get_user(request, "Employee")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    info = {   
        "name": user.username,
        "kind": "Employee",
        "user": user,
    }
    if request.method == 'POST':
        form = CreatePurchaseOrderForm(data=request.POST)
        if form.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.commissioned_employee = user
            purchase_order.save()
            # return redirect(reverse("purchaseorder_home", kwargs={"kind": "Employee"}))
            return redirect(reverse("purchaseorder_home"))
    elif request.method == 'GET':
        form = CreatePurchaseOrderForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)
    return render(request, 'business/create_purchaseorder.html', {"form": form, "info": info})

def delete_purchaseorder(request, order_id):
    user= get_user(request, "Employee")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    purchaseOrder = PurchaseOrder.objects.get(order_id=order_id)
    purchaseOrder.delete_order()
    #返回等待修改
    return redirect(reverse("purchaseorder_home"))

def purchaseorder_home(request):
    user = get_user(request, "Employee")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    info = {
        "name": user.username,
        "kind": "Employee",
        "user": user,
    }
    q = Q(commissioned_employee=user)
    print(q)
    is_search = False
    search_key = ""
    if request.method == 'POST':
        search_key = request.POST.get("search_key")
        if search_key:
            is_search = True
    context = {
        "info": info,
    }
    context["search_key"] = ""
    if is_search:
        context["search_key"] = search_key
        q = q & (Q(id__icontains=search_key))
    context["order_list"] = PurchaseOrder.objects.filter(q).order_by('order_date')
    return render(request, 'business/purchaseorder.html', context)

def view_order_detail(request,order_id):
    user = get_user(request, "Employee")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    info = {
        "name": user.username,
        "kind": "Employee",
        "user": user,
    }
    purchaseOrder = PurchaseOrder.objects.get(order_id=order_id)
    context = {
        "info": info,
    }
    context["purchaseorder"] = purchaseOrder
    return render(request, 'business/purchaseorder_detial.html', context)
class sub_update_order(UpdateView):
    model = PurchaseOrder
    form_class = UpdatePurchaseOrderForm
    template_name = 'business/update_purchaseorder.html'

    def get_context_data(self, **kwargs):
        context = super(sub_update_order,self).get_context_data(**kwargs)
        context.update(kwargs)
        context['info'] = {
            "name": self.request.session.get('user', ''),
            "kind": "Employee",
        }
        return context
    
    def get_success_url(self):
        pass
        return reverse_lazy('purchaseorder_home')

def update_order(request,order_id):
    user = get_user(request, "Employee")
    if not user:
        pass
        return redirect(reverse("login", kwargs={"kind": "Employee"}))
    func = sub_update_order.as_view()
    pk = order_id
    return func(request,pk=pk)
    