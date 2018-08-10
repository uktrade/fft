import django_tables2 as tables
from .models import NaturalCode
from django_tables2.utils import A

from core.tables import FadminTable


class NaturalCodeTable(FadminTable):

    nac_category_description = tables.Column(verbose_name='Category', accessor='NAC_category.NAC_category_description')
    budget_description = tables.Column(verbose_name='Budget Category', accessor='dashboard_grouping.grouping_description')
    dashboard_grouping__linked_budget_code = tables.Column(verbose_name='Budget Code', accessor='dashboard_grouping.linked_budget_code')

    class Meta(FadminTable.Meta):
        model = NaturalCode
        fields = ('nac_category_description',
                  'budget_description',
                  'natural_account_code',
                  'natural_account_code_description',
                  )


