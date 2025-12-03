from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from employees.models import Employee, Department
from leaves.models import LeaveRequest


def dashboard_context():
    return {
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'pending_leaves': LeaveRequest.objects.filter(status='PENDING').count(),
    }


@login_required
def dashboard(request):
    role = request.user.role
    context = dashboard_context()

    # ==========================================
    # 🔥 Detect if logged-in employee is a MANAGER
    # ==========================================
    managed_department = None
    try:
        employee = Employee.objects.get(user=request.user)
        managed_department = Department.objects.filter(manager=employee).first()
    except Employee.DoesNotExist:
        pass

    # ==========================================
    # 🧩 ADMIN DASHBOARD
    # ==========================================
    if role == "ADMIN":
        context["leaves"] = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        context["employees"] = Employee.objects.select_related("user", "designation")
        return render(request, "dashboard/admin_dashboard.html", context)

    # ==========================================
    # 🧩 HR DASHBOARD
    # ==========================================
    if role == "HR":
        context["leaves"] = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        context["employees"] = Employee.objects.select_related("user", "designation")
        context["show_payroll"] = request.GET.get("show_payroll") == "true"
        return render(request, "dashboard/hr_dashboard.html", context)

    # ==========================================
    # 🔥 MANAGER DASHBOARD
    # ==========================================
    if managed_department is not None:
        team = Employee.objects.filter(department=managed_department)
        context["managed_department"] = managed_department
        context["team"] = team
        return render(request, "dashboard/manager_dashboard.html", context)

    # ==========================================
    # 👤 EMPLOYEE DASHBOARD
    # ==========================================
    return render(request, "dashboard/employee_dashboard.html", context)


@login_required
def stats_api(request):
    data = (
        Department.objects
        .annotate(count=Count('employee'))
        .values('name', 'count')
    )
    from django.http import JsonResponse
    return JsonResponse(list(data), safe=False)
