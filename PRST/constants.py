from userApp.models import Employee, Administrator,CommissionedEmployee
from businessApp.models import TimeCard, PurchaseOrder
import businessApp.models
INVALID_KIND = "Invalid kind.kind should be employee or adminster."
INVALID_REQUEST_METHOD = "Invalid request method."
def calculate_salary(employee_id, start_date, end_date):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        raise ValueError(f'No employee found with id {employee_id}')

    # 对于月薪员工
    if employee.hour_or_month == 'Monthly':
        salary = employee.monthly_salary
    # 对于小时工
    elif employee.hour_or_month == 'Hourly':
        # 获取指定日期范围内的时间卡
        timecards = TimeCard.objects.filter(employee=employee, work_date__range=(start_date, end_date))

        # 初始化总工资为0
        total_salary = 0

        for timecard in timecards:
            regular_hours = min(timecard.hours_worked, 8)  # 正常工作小时（最多8小时）
            overtime_hours = max(timecard.hours_worked - 8, 0)  # 加班小时

            # 计算每张时间卡的工资，正常小时按正常费率计算，加班小时按1.5倍费率计算
            total_salary += (regular_hours * employee.hourly_rate) + (overtime_hours * employee.hourly_rate * 1.5)

        salary = total_salary
    else:
        raise ValueError(f'Invalid payment type for employee {employee_id}')

    # 如果员工是佣金员工，添加佣金到工资中
    if isinstance(employee, CommissionedEmployee):
        # 获取指定日期范围内的采购订单
        purchase_orders = PurchaseOrder.objects.filter(commissioned_employee=employee, order_date__range=(start_date, end_date))
        total_sales_amount = sum(order.order_amount for order in purchase_orders)
        commission = total_sales_amount * employee.commission_rate
        salary += commission

    # 如果需要，可以在此处应用其他工资调整或扣除
    # ...

    return salary