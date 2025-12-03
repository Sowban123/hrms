from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from accounts.models import User
from .models import Employee, Department
from .forms import EmployeeCreateForm


@login_required
def employee_list(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    employees = Employee.objects.select_related("user", "department", "designation")
    return render(request, "employees/list.html", {"employees": employees})


@login_required
def create_employee(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # 1) Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                role="EMPLOYEE"
            )

            # 2) Create employee with form data
            Employee.objects.create(
                user=user,
                department=form.cleaned_data["department"],
                designation=form.cleaned_data["designation"],
                date_of_joining=form.cleaned_data["date_of_joining"],
                basic_salary=form.cleaned_data["basic_salary"]
            )

            messages.success(request, "Employee created successfully!")
            return redirect("employees:employee_list")   # go to list after creation

    else:
        form = EmployeeCreateForm()

    return render(request, "employees/create.html", {"form": form})


# 🔥 NEW: Assign / change manager for each department
@login_required
def manage_departments(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    if request.method == "POST":
        dept_id = request.POST.get("department_id")
        manager_id = request.POST.get("manager_id")

        try:
            department = Department.objects.get(id=dept_id)
        except Department.DoesNotExist:
            messages.error(request, "Invalid department selected.")
            return redirect("employees:manage_departments")

        if manager_id:
            try:
                manager = Employee.objects.get(id=manager_id)
            except Employee.DoesNotExist:
                messages.error(request, "Invalid manager selected.")
                return redirect("employees:manage_departments")

            department.manager = manager
        else:
            # remove manager
            department.manager = None

        department.save()
        messages.success(request, f"Manager updated for {department.name}.")
        return redirect("employees:manage_departments")

    # GET: show all departments with possible managers
    departments = Department.objects.prefetch_related("employee_set", "manager")
    return render(request, "employees/departments.html", {"departments": departments})
