from typing import Any
from django.views.generic import CreateView,FormView,DetailView,UpdateView
from django.shortcuts  import reverse,redirect

from userApp.models import Employee,Administrator
from userApp.forms import EmpRegisterForm,AdminRegisterForm,EmpShowForm,AdminShowForm
import random


class CreateEmployeeView(CreateView):
    model = Employee
    form_class = EmpRegisterForm
    template_name = 'user/register.html'
    success_url = 'login'

    def form_valid(self, form):
        print("in form_valid")
        #tmp_username = form.cleaned_data['username']
        new_employee = form.save(commit=False)
        new_employee.save()
        form.save_m2m()
        self.object = new_employee
        tmp_id = new_employee.id
        from_url = "register"
        base_url = reverse(self.get_success_url(),kwargs={'kind':"Employee"})
        return redirect(base_url+"?id="+str(tmp_id)+"&from="+from_url+"&id="+str(tmp_id))
    

class CreateAdminView(CreateView):
    model = Administrator
    form_class = AdminRegisterForm
    template_name = 'user/register.html'
    success_url = 'login'

    def form_valid(self, form):
        new_admin = form.save(commit=False)
        new_admin.save()
        form.save_m2m()

        self.object = new_admin
        tmp_id = new_admin.id
        from_url = "register"
        base_url = reverse(self.get_success_url(),kwargs={'kind':"Administrator"})
        return redirect(base_url+"?id="+str(tmp_id)+"&from="+from_url+"&id="+str(tmp_id))


class DetailEmpView(UpdateView):
    model = Employee
    form_class = EmpShowForm
    template_name = 'user/update.html'

    def get_context_data(self, **kwargs):
        context = super(DetailEmpView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context['kind'] = "Employee"
        return context
    
    def get_success_url(self):
        return reverse("business",kwargs={'kind':"Employee"})


class DetailAdminView(DetailView):
    model = Administrator
    form_class = AdminShowForm
    template_name = 'user/update.html'

    def get_context_data(self, **kwargs):
        context = super(DetailAdminView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context['kind'] = "Administrator"
        return context