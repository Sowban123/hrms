from django.urls import path
from . import views

app_name = "leaves"

urlpatterns = [
    path('', views.leave_list, name='list'),               # employee view
    path('apply/', views.apply_leave, name='apply'),       # employee view
    path('manage/', views.admin_leave_list, name='admin_list'),  # admin/hr view
    path('<int:pk>/approve/', views.approve_leave, name='approve'),
    path('<int:pk>/reject/', views.reject_leave, name='reject'),
]

