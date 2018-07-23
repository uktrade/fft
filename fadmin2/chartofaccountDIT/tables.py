import django_tables2 as tables
from .models import NaturalCode
from django_tables2.utils import A


class NaturalCodeTable(tables.Table):

    class Meta:
        model = NaturalCode
        fields = ('natural_account_code', 'natural_account_code_description','account_L5_code__economic_budget_code')
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no NAC matching the search criteria..."


