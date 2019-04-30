from core.exportutils import get_fk_value
from treasuryCOA.exportcsv import EXPORT_L5_ITERATOR_HEADERS, full_l5_obj

EXPORT_NAC_ITERATOR_HEADERS = EXPORT_L5_ITERATOR_HEADERS + [
        'Level 6',
        'Level 6 Description',
        'used for budget',
        'Budget Category',
        'Budget Grouping',
        'Commercial Category',
        'account L5 code',
        'account L5 description',
        'Economic Budget Code',
        'Budget/Forecast NAC',
        'L5 code for OSCAR upload',
        'L5 description for OSCAR upload',
        'Expenditure Type'
    ]

def _export_nac_iterator(queryset):
    yield EXPORT_NAC_ITERATOR_HEADERS

    for obj in queryset:
        yield full_l5_obj(obj.account_L5_code) + [
               obj.natural_account_code,
               obj.natural_account_code_description,
               obj.used_for_budget,
               get_fk_value(obj.expenditure_category, 'grouping_description'),
               get_fk_value(obj.expenditure_category.NAC_category, 'NAC_category_description') if obj.expenditure_category else '-',
               get_fk_value(obj.commercial_category, 'commercial_category'),
               get_fk_value(obj.expenditure_category.NAC_category, 'NAC_category_description') if obj.expenditure_category else '-',
               get_fk_value(obj.account_L5_code_upload, 'account_l5_code'),
               get_fk_value(obj.account_L5_code_upload, 'account_l5_long_name'),
               obj.active
               ]


def _export_historical_nac_iterator(queryset):
    yield [
                'Level 6',
                'Level 6 Description',
                'used for budget',
                'Budget Category',
                'Budget Grouping',
                'Commercial Category',
                'account L5 code',
                'account L5 description',
                'Budget/Forecast NAC',
                'L5 for OSCAR upload',
                'Expenditure Type',
                'active',
                'financial year',
                'archived'
            ]
    for obj in queryset:
        yield [
                obj.natural_account_code,
                obj.natural_account_code_description,
                obj.used_for_budget,
                obj.expenditure_category,
                obj.NAC_category,
                obj.commercial_category,
                obj.account_L5_code,
                obj.account_L5_description,
                obj.account_L6_budget,
                obj.account_L5_code_upload,
                obj.economic_budget_code,
                obj.active,
                obj.financial_year.financial_year_display,
                obj.archived
        ]


def _export_exp_cat_iterator(queryset):
    yield ['Budget Grouping', 'Expenditure Category',
           'Description', 'Further Description', 'Budget NAC', 'Budget NAC Description'
           ]
    for obj in queryset:
        yield [obj.NAC_category.NAC_category_description,
               obj.grouping_description,
               obj.description,
               obj.further_description,
               obj.linked_budget_code.natural_account_code,
               obj.linked_budget_code.natural_account_code_description]


def _export_historical_exp_cat_iterator(queryset):
    yield [
        'Budget Category',
        'description',
        'further description',
        'Budget Code',
        'Budget Description',
        'Budget Grouping',
        'financial year',
        'archived',
        ]
    for obj in queryset:
        yield [
            obj.grouping_description,
            obj.description,
            obj.further_description,
            obj.linked_budget_code,
            obj.linked_budget_code_description,
            obj.NAC_category,
            obj.financial_year.financial_year_display,
            obj.archived
        ]


def _export_comm_cat_iterator(queryset):
    yield ['Commercial Category',
           'Description', 'Approvers'
           ]
    for obj in queryset:
        yield [obj.commercial_category,
               obj.description,
               obj.approvers
               ]


def _export_historical_comm_cat_iterator(queryset):
    yield ['Commercial Category',
           'Description',
           'Approvers',
           'financial year',
           'archived'
           ]
    for obj in queryset:
        yield [obj.commercial_category,
               obj.description,
               obj.approvers,
               obj.financial_year.financial_year_display,
               obj.archived]


def _export_nac_cat_iterator(queryset):
    yield ['Budget Grouping']

    for obj in queryset:
        yield [obj.NAC_category_description, ]


def _export_programme_iterator(queryset):
    yield ['Programme Code', 'Description', 'Budget Type', 'Active']
    for obj in queryset:
        yield [obj.programme_code,
               obj.programme_description,
               obj.budget_type,
               obj.active]


def _export_programme_iterator(queryset):
    yield ['Programme Code', 'Description', 'Budget Type', 'Active', 'Financial Year', 'Archived Date']
    for obj in queryset:
        yield [obj.programme_code,
               obj.programme_description,
               obj.budget_type,
               obj.active,
               obj.financial_year.financial_year_display,
               obj.archived
               ]


def _export_inter_entity_l1_iterator(queryset):
    yield ['L1 Value', 'L1 Description'
           ]
    for obj in queryset:
        yield [obj.l1_value,
               obj.l1_description
               ]


def _export_fco_mapping_iterator(queryset):
    yield ['FCO (Prism) Code', 'FCO (Prism) Description',
           'Oracle (DIT) Code', 'Oracle (DIT) Description','Active']
    for obj in queryset:
        yield [obj.fco_code,
               obj.fco_description,
               obj.account_L6_code_fk.natural_account_code,
               obj.account_L6_code_fk.natural_account_code_description,
               obj.active]


def _export_historical_fco_mapping_iterator(queryset):
    yield ['FCO (Prism) Code',
           'FCO (Prism) Description',
           'Oracle (DIT) Code',
           'Oracle (DIT) Description',
           'Budget Grouping',
           'Budget Category',
           'Expenditure Type',
           'Active',
           'Financial Year',
           'Archived Date']
    for obj in queryset:
        yield [obj.fco_code,
               obj.fco_description,
               obj.account_L6_code,
               obj.account_L6_description,
               obj.nac_category_description,
               obj.budget_description,
               obj.economic_budget_code,
               obj.active,
               obj.financial_year.financial_year_display,
               obj.archived
               ]


def _export_inter_entity_iterator(queryset):
    yield ['L1 Value',
           'L1 Description',
           'L2 Value',
           'L2 Description',
           'CPID',
           'Active'
           ]
    for obj in queryset:
        yield [obj.l1_value.l1_value,
               obj.l1_value.l1_description,
               obj.l2_value,
               obj.l2_description,
               obj.cpid,
               obj.active]


def _export_historical_inter_entity_iterator(queryset):
    yield [
            'Government Body',
            'Government Body Description',
            'ORACLE - Inter Entity Code',
            'ORACLE - Inter Entity Description',
            'Treasury - CPID (Departmental Code No.)',
            'active',
            'financial year',
            'archived',
    ]
    for obj in queryset:
        yield [
            obj.l1_value,
            obj.l1_description,
            obj.l2_value,
            obj.l2_description,
            obj.cpid,
            obj.active,
            obj.financial_year.financial_year_display,
            obj.archived
        ]


