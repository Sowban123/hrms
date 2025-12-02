from django import forms
from accounts.models import User
from .models import Employee

class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['department', 'designation', 'date_of_joining', 'basic_salary']
