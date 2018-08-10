from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from .models import DepartmentalGroup, Directorate, CostCentre

from .tables import CostCentreTable, DirectorateTable, DepartmentalGroupTable
from .filters import CostCentreFilter


class FilteredCostListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = CostCentreTable
    model = CostCentre
    paginate_by = 50
    template_name = 'core/table_filter_generic.html'
    filterset_class = CostCentreFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Cost Centres'
        return context


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


def costcentre(request):
    table = CostCentreTable(CostCentre.objects.filter(active=True))
    RequestConfig(request).configure(table)
    return render(request, 'costcentre/costcentre.html', {'table': table})


# def directorate(request):
#     table = DirectorateTable(Directorate.objects.all())
#     RequestConfig(request).configure(table)
#     return render(request, 'costcentre/directorate.html', {'table': table})


class DirectorateList(SingleTableView):
    model = Directorate
    table_class = DirectorateTable
    template_name = 'costcentre/directorate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'AAAA'
        return context


def departmentalgroup(request):
    table = DepartmentalGroupTable(DepartmentalGroup.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'costcentre/departmentalgroup.html', {'table': table})


class DirectorateListView(generic.ListView):
    # see if there is an argument groupcode
    # Directorate.objects.filter(group_code__group_code='1091HT')
    # def get_queryset(self):
    #         return Directorate.objects.filter(lab__acronym=self.kwargs['lab'])
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context
    model = Directorate
    ordering = ['group_code']

    def get_queryset(self):
        group = self.kwargs.get('group', 'all')
        if group == 'all':
            return Directorate.objects.all()
        else:
            return Directorate.objects.filter(group__group_code=group)


class DepartmentalGroupListView(generic.ListView):
    model = DepartmentalGroup

