from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Employee

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee(sender, instance, created, **kwargs):
    """
    Automatically create Employee profile ONLY when:
    - The user is created for the first time, AND
    - The user role is EMPLOYEE
    """
    if not created:   # only on first creation
        return

    if instance.role != "EMPLOYEE":
        return  # Do NOT create employee for HR or ADMIN

    Employee.objects.get_or_create(
        user=instance,
        defaults={
            "date_of_joining": "2000-01-01",
            "basic_salary": 0,
        }
    )
