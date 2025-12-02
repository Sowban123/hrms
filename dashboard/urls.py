from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),               # auto-redirect based on role
    path('stats/', views.stats_api, name='stats_api'),         # used only by admin chart
]
