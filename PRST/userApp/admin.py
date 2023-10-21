from django.contrib import admin
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DateRangeForm
import csv
# Register your models here.
from .models import *
from constants import calculate_salary
from businessApp.models import TimeCard, PurchaseOrder


# def export_reports(modeladmin, request, queryset):
#     print("export_reports")
#     form = None
#     print(request.POST)
#     if 'apply' in request.POST:
#         print("export_reports 0")
#         form = DateRangeForm(request.POST)
#         print("export_reports 1")
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             print("export_reports 2") 
#             # 创建一个HTTP响应对象，以便将CSV文件发送到客户端
#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = f'attachment; filename="reports.csv"'

#             writer = csv.writer(response)

#             # 写入CSV文件的标题行
#             writer.writerow(['Employee Name', 'Total Work Hours', 'Total Commission', 'Total Salary'])

#             for user in queryset:
#                 start_date = timezone.now() - timezone.timedelta(days=30)  # 例如，获取过去30天的数据
#                 end_date = timezone.now()
#                 timecard = TimeCard.objects.filter(employee=user, work_date__range=(start_date, end_date))
#                 total_work_hours = sum(timecardone.hours_worked for timecardone in timecard)
#                 if isinstance(user, CommissionedEmployee):
#                     purchase_orders = PurchaseOrder.objects.filter(commissioned_employee=user, order_date__range=(start_date, end_date))
#                     total_sales_amount = sum(order.order_amount for order in purchase_orders)
#                     total_commission = total_sales_amount * user.commission_rate
#                 else:
#                     total_commission = 0
#                 total_salary = calculate_salary(user.id, start_date, end_date)
#                 writer.writerow([user.name, total_work_hours, total_commission, total_salary])
#                 print("export_reports 3") 
#                 print(response)
#             return response
#         else:
#             print(form.errors)
#     if not form:
#         print("export_reports 4")
#         form = DateRangeForm(auto_id='%s')

#     return render(request, 'admin/export_reports.html', {'form': form})

# export_reports.short_description = 'Export Reports for selected employees'
def export_reports(modeladmin, request, queryset):
    # 设定日期范围从2000年1月1日到现在
    start_date = timezone.datetime(2000, 1, 1, tzinfo=timezone.utc)
    end_date = timezone.now()

    # 创建一个HTTP响应对象，以便将CSV文件发送到客户端
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reports.csv"'

    writer = csv.writer(response)

    # 写入CSV文件的标题行
    writer.writerow(['Employee Name', 'Total Work Hours', 'Total Commission', 'Total Salary'])

    for user in queryset:
        timecard = TimeCard.objects.filter(employee=user, work_date__range=(start_date, end_date))
        total_work_hours = sum(timecardone.hours_worked for timecardone in timecard)
        if isinstance(user, CommissionedEmployee):
            purchase_orders = PurchaseOrder.objects.filter(commissioned_employee=user, order_date__range=(start_date, end_date))
            total_sales_amount = sum(order.order_amount for order in purchase_orders)
            total_commission = total_sales_amount * user.commission_rate
        else:
            total_commission = 0
        total_salary = calculate_salary(user.id, start_date, end_date)
        writer.writerow([user.name, total_work_hours, total_commission, total_salary])

    return response  # 返回响应对象，其中包含CSV文件

export_reports.short_description = 'Export Reports for selected employees'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    actions = [export_reports]

class CommissionedEmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(CommissionedEmployee,CommissionedEmployeeAdmin)
#admin.site.register(Administrator)