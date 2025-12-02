from django.db import models
from employees.models import Employee

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    working_days = models.IntegerField(default=30)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    lop_days = models.IntegerField(default=0)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')   # Prevent duplicate payroll
