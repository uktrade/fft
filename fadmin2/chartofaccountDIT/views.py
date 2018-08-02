
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import NACCategory, NaturalCode, Analysis1, Analysis2, NACDashboardGrouping

from .tables import NaturalCodeTable
from django_tables2 import RequestConfig


def naturalcode(request):
#    table = NaturalCodeTable(NaturalCode.objects.filter(used_by_DIT=True).values('account_L5_code__account_l5_long_name'))
    table = NaturalCodeTable(NaturalCode.objects.filter(used_by_DIT=True).values('natural_account_code',
                                                                                 'natural_account_code_description',
                                                                                 'NAC_category__NAC_category_description',
                                                                                 'dashboard_grouping__grouping_description',
                                                                                 'account_L5_code__economic_budget_code'))


    RequestConfig(request, paginate={'per_page': 50}).configure(table)
    return render(request, 'chartofaccountDIT/naturalcode.html', {'table': table})

