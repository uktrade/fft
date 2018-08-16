import django_tables2 as tables
from .models import NaturalCode

from core.tables import FadminTable


class NaturalCodeTable(FadminTable):

    nac_category_description = tables.Column(verbose_name='Budget Grouping', accessor='NAC_category.NAC_category_description')
    budget_description = tables.Column(verbose_name='Expenditure Category', accessor='dashboard_grouping.grouping_description')
    dashboard_grouping__linked_budget_code = tables.Column(verbose_name='PRIME NAC for Budget/Forecast', accessor='dashboard_grouping.linked_budget_code')
    account_L5_code__economic_budget_code = tables.Column(verbose_name='Expenditure Type', accessor ='account_L5_code.economic_budget_code')

    class Meta(FadminTable.Meta):
        model = NaturalCode
        fields = ('account_L5_code__economic_budget_code',
                  'nac_category_description',
                  'budget_description',
                  'dashboard_grouping__linked_budget_code',
                  'natural_account_code',
                  'natural_account_code_description',
                  )


