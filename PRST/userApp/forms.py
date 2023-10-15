from django import forms
from userApp.models import Employee,Administrator


class EmpLoginFrom(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class AdminLoginFrom(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))