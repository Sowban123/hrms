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

def create_employee(request):
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            # Create User
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User.objects.create_user(
                username=username,
                password=password,
                role="EMPLOYEE"
            )

            # Create Employee linked to User
            emp = form.save(commit=False)
            emp.user = user
            emp.save()

            messages.success(request, "Employee created successfully!")
            return redirect("dashboard")

    else:
        form = EmployeeCreateForm()

    return render(request, "employees/create.html", {"form": form})
