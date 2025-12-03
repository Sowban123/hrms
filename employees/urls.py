from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('create/', views.create_employee, name='create'),
    path('departments/', views.manage_departments, name='manage_departments'),  # 🔥 NEW
]
