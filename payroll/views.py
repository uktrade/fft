from django.shortcuts import render

def payroll_list(request):
    return render(request, 'payroll/list/list.html')

def payroll_edit(request):
    return render(request, 'payroll/edit/edit.html')