# 在你的应用目录中创建一个名为 report_generation.py 的新文件

import csv
from datetime import timedelta
from django.utils import timezone
from .models import CommissionedEmployee,Employee
from businessApp.models import TimeCard, PurchaseOrder
from constants import calculate_salary  # 确保正确导入
import os

def generate_weekly_report():
    # 获取上一周的开始和结束日期
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    save_directory = os.path.join(os.path.dirname(__file__), 'management/commands/save')
    os.makedirs(save_directory, exist_ok=True)

    # 创建一个CSV文件
    file_name = f'report_{start_date.strftime("%Y-%m-%d")}_to_{end_date.strftime("%Y-%m-%d")}.csv'
    file_path = os.path.join(save_directory, file_name)
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 写入CSV文件的标题行
        writer.writerow(['Employee Name', 'Total Work Hours', 'Total Commission', 'Total Salary'])

        # 获取所有员工
        all_employees = Employee.objects.all()
        print(all_employees.count())
        for user in all_employees:
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

    return file_path  # 返回生成的文件名，以便于测试和调试
