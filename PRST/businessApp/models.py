from django.db import models
from userApp.models import CommissionedEmployee,Employee
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from django.utils import timezone

class PurchaseOrder(models.Model):
    order_id = models.AutoField(primary_key=True)  # 自动生成的唯一订单ID
    commissioned_employee = models.ForeignKey(CommissionedEmployee, on_delete=models.CASCADE)  # 与委托员工相关联
    client_contact = models.CharField(max_length=200)  # 客户的联系点
    client_billing_address = models.CharField(max_length=255)  # 客户的计费地址
    purchased_products = models.TextField()  # 购买的产品列表
    order_date = models.DateField()  # 订单日期
    order_amount = models.FloatField()  # 订单金额

    def create_order(self, employee, client_contact, client_billing_address, purchased_products, order_amount):
        self.commissioned_employee = employee
        self.client_contact = client_contact
        self.client_billing_address = client_billing_address
        self.purchased_products = purchased_products
        self.order_amount = order_amount
        self.save()
        return self.order_id

    def update_order(self, updated_info: dict):
        for key, value in updated_info.items():
            setattr(self, key, value)
        self.save()

    def delete_order(self):
        self.delete()

    def calculate_commission(self):
        # 假设commission_rate是一个小数，例如0.05代表5%的佣金率
        return self.order_amount * self.commissioned_employee.commission_rate
    
    def __str__(self):
        return f"Order ID: {self.order_id}, Created by: {self.commissioned_employee.name}"


class TimeCard(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # 关联的员工
    work_date = models.DateField()  # 工作日期
    start_time = models.TimeField()  # 开始工作时间
    end_time = models.TimeField()  # 结束工作时间
    is_submitted = models.BooleanField(default=False)  # 是否已提交
    submitted_date = models.DateField( null=True, blank=True)  # 提交日期

    class Meta:
        unique_together = ('employee', 'work_date')  # 同一天只能有一张时间卡

    def __str__(self):
        return f"{self.employee.name} - {self.work_date}"

    def clean(self):
        super().clean()
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')

         # 获取员工的最大工作时长
        max_hours = self.employee.hour_limit
        if max_hours is not None:
        # 计算实际工作时长
            delta = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, self.start_time)
            hours_worked = delta.seconds / 3600
        # 如果实际工作时长超过最大时长，则自动设置为最大时长
            if hours_worked > max_hours:
                adjusted_end_time = datetime.combine(self.work_date, self.start_time) + timedelta(hours=max_hours)
                self.end_time = adjusted_end_time.time()

    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def submit_timecard(self):
        if not self.is_submitted:
            self.is_submitted = True
            self.submitted_date = timezone.now().date()
            self.save()

    @property
    def hours_worked(self):
        # 计算以小时为单位的工作时间
        delta = datetime.combine(date.min, self.end_time) - datetime.combine(date.min, self.start_time)
        return delta.seconds / 3600

    @classmethod
    def employee_total_hours(cls, employee, start_date, end_date):
        # 计算在指定日期范围内员工的总工作时间
        timecards = cls.objects.filter(employee=employee, work_date__range=(start_date, end_date))
        return sum(timecard.hours_worked for timecard in timecards)