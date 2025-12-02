from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from employees.models import Employee, Department
from leaves.models import LeaveRequest


# common context for all roles
def dashboard_context():
    return {
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'pending_leaves': LeaveRequest.objects.filter(status='PENDING').count(),
    }


# redirect user to correct dashboard based on role
@login_required
def dashboard(request):
    role = request.user.role
    context = dashboard_context()

    if role in ["ADMIN", "HR"]:
        context["leaves"] = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        context["employees"] = Employee.objects.select_related("user", "designation").all()

    return render(
        request,
        f"dashboard/{role.lower()}_dashboard.html",
        context
    )


# API for admin chart
@login_required
def stats_api(request):
    data = (
        Department.objects
        .annotate(count=Count('employee'))
        .values('name', 'count')
    )
    from django.http import JsonResponse
    return JsonResponse(list(data), safe=False)
