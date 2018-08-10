
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django_tables2.views import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig

from .models import NACCategory, NaturalCode, Analysis1, Analysis2, NACDashboardGrouping

from .tables import NaturalCodeTable
from .filters import NACFilter


class FilteredNACListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = NaturalCodeTable
    model = NaturalCode
    paginate_by = 50
    template_name = 'core/table_filter_generic.html'
    filterset_class = NACFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Natural Account Codes'
        return context



def naturalcode(request):
#    table = NaturalCodeTable(NaturalCode.objects.filter(used_by_DIT=True).values('account_L5_code__account_l5_long_name'))
    table = NaturalCodeTable(NaturalCode.objects.filter(used_by_DIT=True).values('dashboard_grouping__linked_budget_code',
                                                                                 'natural_account_code',
                                                                                 'natural_account_code_description',
                                                                                 'NAC_category__NAC_category_description',
                                                                                 'dashboard_grouping__grouping_description',
                                                                                 'account_L5_code__economic_budget_code'))

    RequestConfig(request, paginate={'per_page': 50}).configure(table)
    return render(request, 'chartofaccountDIT/naturalcode.html', {'table': table})

