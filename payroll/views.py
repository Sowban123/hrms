from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from calendar import monthrange
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from xhtml2pdf import pisa

from .models import Payroll
from employees.models import Employee
from attendance.models import Attendance
from leaves.models import LeaveRequest
from accounts.decorators import role_required  # Ensure this exists


# ------------------ PAYROLL LIST ------------------ #
@login_required
def payroll_list(request):
    qs = Payroll.objects.select_related("employee")
    if request.user.role == "EMPLOYEE":
        qs = qs.filter(employee__user=request.user)

    records = qs.order_by("-year", "-month")
    return render(request, "payroll/list.html", {"records": records})


# ------------------ PAYSLIP PDF ------------------ #
@login_required
def payslip_pdf(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    # Prevent unauthorized access
    if request.user.role == "EMPLOYEE" and payroll.employee.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    template = get_template("payroll/payslip.html")
    html = template.render({"payroll": payroll})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="payslip_{payroll.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response


# ------------------ GENERATE PAYROLL ------------------ #
@login_required
@role_required(["ADMIN", "HR"])
def generate_payroll(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == "POST":
        month = int(request.POST.get("month"))
        year = int(request.POST.get("year"))

        # Avoid duplicate payrolls
        if Payroll.objects.filter(employee=employee, month=month, year=year).exists():
            messages.error(request, "Payroll already generated for this month.")
            return redirect("payroll:list")

        # Actual working days
        working_days = monthrange(year, month)[1]

        # Attendance count
        # Attendance count (use user, NOT employee)
        present_days = Attendance.objects.filter(
           user=employee.user,
           date__year=year,
           date__month=month
           ).count()
       

        absent_days = working_days - present_days


        # LOP days calculation for multi-day leaves
        lop_days = LeaveRequest.objects.filter(
            employee=employee,
            status="APPROVED",
            leave_type="LOP",
            start_date__year=year,
            start_date__month=month,
        ).annotate(
            duration=ExpressionWrapper(F("end_date") - F("start_date") + 1, IntegerField())
        ).aggregate(total=Sum("duration"))["total"] or 0

        per_day_salary = employee.basic_salary / working_days
        deductions = lop_days * per_day_salary
        gross_salary = employee.basic_salary
        net_salary = gross_salary - deductions

        Payroll.objects.create(
            employee=employee,
            month=month,
            year=year,
            basic_salary=employee.basic_salary,
            working_days=working_days,
            present_days=present_days,
            absent_days=absent_days,
            lop_days=lop_days,
            gross_salary=gross_salary,
            deductions=deductions,
            net_salary=net_salary,
        )

        messages.success(request, "Payroll generated successfully!")
        return redirect("payroll:list")

    return render(request, "payroll/generate.html", {"employee": employee})
