from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import DepartmentalGroup, Directorate, CostCentre



def index(request):
    num_group = DepartmentalGroup.objects.all().count()
    num_directorate = Directorate.objects.all().count()
    num_costcentre = CostCentre.objects.all().count()

    return render (
        request,
        'index.html',
        context={'num_group':num_group,
                 'num_directorate': num_directorate,
                 'num_costcentre': num_costcentre
                 }
    )


class CostcentreListView(generic.ListView):
    model = CostCentre

