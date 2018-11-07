from core.tables import FadminTable

import django_tables2 as tables

from .models import Analysis1, Analysis2, \
    CommercialCategory, ExpenditureCategory, InterEntity, NaturalCode, ProgrammeCode


class ProgrammeTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = ProgrammeCode
        fields = (
            'programme_code',
            'programme_description',
            'budget_type'
        )


class NaturalCodeTable(FadminTable):
    nac_category_description = \
        tables.Column(verbose_name='Budget Grouping',
                      accessor='expenditure_category.NAC_category.NAC_category_description')
    budget_description = tables.Column(verbose_name='Budget Category',
                                       accessor='expenditure_category.grouping_description')
    budget_NAC_code = tables.Column(verbose_name='Budget/Forecast NAC',
                                    accessor='expenditure_category.linked_budget_code.natural_account_code')  # noqa: E501
    account_L5_code__economic_budget_code = \
        tables.Column(verbose_name='Expenditure Type',
                      accessor='account_L5_code.economic_budget_code')
    natural_account_code = tables.Column(verbose_name='PO/Actuals NAC')
    natural_account_code_description = tables.Column(verbose_name='NAC Description')

    class Meta(FadminTable.Meta):
        model = NaturalCode
        fields = ('account_L5_code__economic_budget_code',
                  'nac_category_description',
                  'budget_description',
                  'commercial_category',
                  'budget_NAC_code',
                  'natural_account_code',
                  'natural_account_code_description',
                  )


class ExpenditureCategoryTable(FadminTable):
    nac_category = tables.Column(verbose_name='Budget Grouping',
                                 accessor='NAC_category.NAC_category_description')

    class Meta(FadminTable.Meta):
        model = ExpenditureCategory
        fields = ('nac_category',
                  'grouping_description',
                  'description',
                  'further_description'
                  )


class CommercialCategoryTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = CommercialCategory
        fields = ('commercial_category',
                  'description'
                  )


class Analysis2Table(FadminTable):
    class Meta(FadminTable.Meta):
        model = Analysis2
        fields = ('analysis2_code',
                  'analysis2_description',
                  )


class Analysis1Table(FadminTable):
    analysis1_description = tables.Column(
                        attrs = {'th': {'id': 'fiftypercent'}})
    class Meta(FadminTable.Meta):
        model = Analysis1
        fields = ('analysis1_code',
                  'analysis1_description',
                  'supplier',
                  'pc_reference'
                  )


class InterEntityTable(FadminTable):
    l1_value__l1_value = \
        tables.Column(verbose_name='L1 Value',
                      accessor='l1_value.l1_value')
    l1_value__l1_description = \
        tables.Column(verbose_name='L1 Description',
                      accessor='l1_value.l1_description')

    class Meta(FadminTable.Meta):
        model = InterEntity
        fields = ('l1_value__l1_value',
                  'l1_value__l1_description',
                  'l2_value',
                  'l2_description',
                  'cpid'
                  )
