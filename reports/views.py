import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from employees.models import Employee

@login_required
def employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Department', 'Designation', 'DOJ', 'Basic Salary'])
    for emp in Employee.objects.select_related('user', 'department', 'designation'):
        writer.writerow([
            emp.user.get_full_name() or emp.user.username,
            emp.department.name if emp.department else '',
            emp.designation.name if emp.designation else '',
            emp.date_of_joining,
            emp.basic_salary,
        ])
    return response

@login_required
def employees_pdf(request):
    employees = Employee.objects.select_related('user', 'department', 'designation')
    template = get_template('reports/employees_pdf.html')
    html = template.render({'employees': employees})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF error')
    return response
