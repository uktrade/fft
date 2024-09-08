from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Payroll

def payroll_list(request):
    return render(request, 'payroll/list/list.html')

def payroll_edit(request):
    return render(request, 'payroll/edit/edit.html')