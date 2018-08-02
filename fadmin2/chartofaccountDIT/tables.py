import django_tables2 as tables
from .models import NaturalCode
from django_tables2.utils import A


class NaturalCodeTable(tables.Table):
    paginate_by = 50
    class Meta:
        model = NaturalCode
        fields = ('natural_account_code',
                  'natural_account_code_description',
                  'NAC_category__NAC_category_description',
                  'dashboard_grouping__grouping_description',
                  'account_L5_code__economic_budget_code')
        template_name = 'django_tables2/bootstrap.html'
        attrs = {"class": "table-striped table-bordered small-font"}
        empty_text = "There are no NAC matching the search criteria..."


