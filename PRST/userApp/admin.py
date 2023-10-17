from django.contrib import admin

# Register your models here.
from .models import *


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CommissionedEmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(CommissionedEmployee,CommissionedEmployeeAdmin)
#admin.site.register(Administrator)