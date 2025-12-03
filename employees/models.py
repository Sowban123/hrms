from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100)

    # 🔥 NEW: each department can have ONE manager (optional)
    manager = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managing_department'
    )

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_joining = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    employee_id = models.CharField(max_length=20, null=True, blank=True)  # keep as is

    def __str__(self):
        return self.user.get_full_name() or self.user.username
