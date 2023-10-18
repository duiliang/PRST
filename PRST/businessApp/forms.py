from django import forms
from .models import Employee, TimeCard, CommissionedEmployee, PurchaseOrder
#from django_flatpickr.widgets import TimePickerInput ,DatePickerInput
#from datetimewidget.widgets import DateTimeWidget, TimeWidget, DateWidget
from bootstrap_datepicker_plus.widgets import TimePickerInput,DatePickerInput
class CreateTimecardForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, widget=forms.HiddenInput())
    class Meta:
        model = TimeCard
        fields = ['work_date', 'start_time', 'end_time','employee']
        # widgets = {
        #     'work_date': DatePickerInput(),
        #     'start_time': TimePickerInput(),
        #     'end_time': TimePickerInput(),
        # }
        widgets = {
            'work_date': forms.SelectDateWidget(),
            'start_time': forms.TimeInput(format='%H:%M'),
            'end_time': forms.TimeInput(format='%H:%M'),
            #'employee': forms.HiddenInput()
        }


class CreatePurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['client_contact', 'client_billing_address', 'purchased_products', 'order_amount', 'order_date']
        widgets = {
            'order_date': DatePickerInput(),
        }

class UpdatePurchaseOrderForm(CreatePurchaseOrderForm):
    class Meta:
        model = PurchaseOrder
        fields = ['client_contact', 'client_billing_address', 'purchased_products', 'order_amount', 'order_date']
        widgets = {
            'order_date': DatePickerInput(),
        }



        
