from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HR', 'HR'),
        ('EMPLOYEE', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_hr(self):
        return self.role == 'HR'

    def is_employee(self):
        return self.role == 'EMPLOYEE'
