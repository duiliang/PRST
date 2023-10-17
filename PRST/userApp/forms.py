from typing import Any
from django import forms
from userApp.models import Employee,Administrator,PAYMENT_METHODS


class EmpLoginForm(forms.Form):
    #username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    id = forms.IntegerField(label="ID", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class AdminLoginForm(forms.Form):
    #username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    id = forms.IntegerField(label="ID", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EmpRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = (
            'name',
            "position",
            'hour_or_month',
            "hourly_rate",
            "monthly_salary",
            "payment_method",
            "payment_address",
            "payment_cardID",
            "username",
            "password",
            "address",
            "phone_number",
            "gender",
            "hour_limit",
        )


    def clean(self) :
        cleaned_data = super(EmpRegisterForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        #print(confirm_password, password)
        if confirm_password != password:
            self._errors['confirm_password'] = self.error_class(['Password does not match.'])
        return cleaned_data


class AdminRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Administrator
        fields = (
            'name',
            "username",
            "password",
            "contact_information",
        )

        
    def clean(self) :
        cleaned_data = super(AdminRegisterForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        #print(confirm_password, password)
        if confirm_password != password:
            self._errors['confirm_password'] = self.error_class(['Password does not match.'])
        return cleaned_data

class EmpShowForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['payment_method', 'payment_address', 'payment_cardID']
        widgets = {
            'payment_method': forms.Select(choices=PAYMENT_METHODS)
        }


class AdminShowForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = '__all__'
    def __init__(self):
        super(EmpShowForm, self).__init__()
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True