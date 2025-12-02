from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee

@login_required
def employee_list(request):
    employees = Employee.objects.select_related('user', 'department', 'designation')
    return render(request, 'employees/list.html', {'employees': employees})

from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User
from .forms import EmployeeCreateForm
from .models import Employee


def create_employee(request):
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=username,
                password=password,
                role="EMPLOYEE"
            )

            employee = Employee.objects.get(user=user)
            employee.department = form.cleaned_data["department"]
            employee.designation = form.cleaned_data["designation"]
            employee.date_of_joining = form.cleaned_data["date_of_joining"]
            employee.basic_salary = form.cleaned_data["basic_salary"]
            employee.save()

            messages.success(request, "Employee created successfully!")
            return redirect("employees:create")     # fixes POST refresh issue

    else:
        form = EmployeeCreateForm()

    return render(request, "employees/create.html", {"form": form})
