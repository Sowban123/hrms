from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from .models import LeaveRequest
from .forms import LeaveRequestForm
from accounts.decorators import role_required
from django.contrib import messages



@login_required
@role_required(["EMPLOYEE"])
def leave_list(request):
    # Get current employee -> show their own requests only
    employee = Employee.objects.get(user=request.user)
    leaves = LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
    return render(request, 'leaves/list.html', {'leaves': leaves})


@login_required
@role_required(["EMPLOYEE"])
def apply_leave(request):
    employee = Employee.objects.get(user=request.user)

    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.status = "PENDING"
            leave.save()
            return redirect('leaves:list')
    else:
        form = LeaveRequestForm()

    return render(request, 'leaves/apply.html', {'form': form})




from accounts.decorators import role_required

@login_required
@role_required(["ADMIN", "HR"])
def admin_leave_list(request):
    leaves = LeaveRequest.objects.select_related("employee").order_by("-created_at")
    return render(request, "leaves/admin_list.html", {"leaves": leaves})


@login_required
@role_required(["ADMIN", "HR"])
def approve_leave(request, pk):
    leave = LeaveRequest.objects.get(id=pk)
    leave.status = "APPROVED"
    leave.approved_by = request.user
    leave.save()
    messages.success(request, "Leave approved successfully")
    return redirect("leaves:admin_list")


@login_required
@role_required(["ADMIN", "HR"])
def reject_leave(request, pk):
    leave = LeaveRequest.objects.get(id=pk)
    leave.status = "REJECTED"
    leave.approved_by = request.user
    leave.save()
    messages.error(request, "Leave rejected")
    return redirect("leaves:admin_list")
