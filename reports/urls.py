from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('employees/csv/', views.employees_csv, name='employees_csv'),
    path('employees/pdf/', views.employees_pdf, name='employees_pdf'),
]
