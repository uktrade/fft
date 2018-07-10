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


class DirectorateListView(generic.ListView):
    # see if there is an argument groupcode
    # Directorate.objects.filter(group_code__group_code='1091HT')
    model = Directorate
    ordering = ['group_code']



class DepartmentalGroupListView(generic.ListView):
    model = DepartmentalGroup

