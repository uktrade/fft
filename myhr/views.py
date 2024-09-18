from django.shortcuts import render

def myhr_list(request):
    return render(request, 'myhr/list/list.html')