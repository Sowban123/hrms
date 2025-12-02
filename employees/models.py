from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100)

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


    def __str__(self):
        return self.user.get_full_name() or self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Employee

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee(sender, instance, created, **kwargs):
    if created and instance.role == 'EMPLOYEE':
        Employee.objects.create(
            user=instance,
            date_of_joining="2000-01-01",  # temporary default
            basic_salary=0
        )
