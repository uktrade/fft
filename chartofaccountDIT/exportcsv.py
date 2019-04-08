from core.exportutils import get_fk_value


def _export_nac_iterator(queryset):
    yield ['Level 6', 'Level 6 Description',
           'Active', 'Level 5', 'Level 5 Description',
           'Category', 'Dashboard Group']

    for obj in queryset:
        yield [obj.natural_account_code,
               obj.natural_account_code_description,
               obj.active,
               get_fk_value(obj.account_L5_code, 'account_l5_code'),
               get_fk_value(obj.account_L5_code, 'account_l5_long_name')]


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


def _export_comm_cat_iterator(queryset):
    yield ['Commercial Category',
           'Description', 'Approvers'
           ]
    for obj in queryset:
        yield [obj.commercial_category,
               obj.description,
               obj.approvers]


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
    yield ['FCO Code', 'FCO Description', 'Oracle L6 Code',
           'Oracle L6 Code', 'Oracle L6 Description','Active']
    for obj in queryset:
        yield [obj.fco_code,
               obj.fco_description,
               obj.account_L6_code_fk.natural_account_code,
               obj.account_L6_code_fk.natural_account_code_description,
               obj.active]


def _export_inter_entity_iterator(queryset):
    yield ['L1 Value', 'L1 Description', 'L2 Value', 'L2 Description',
           'CPID', 'Active'
           ]
    for obj in queryset:
        yield [obj.l1_value.l1_value,
               obj.l1_value.l1_description,
               obj.l2_value,
               obj.l2_description,
               obj.cpid,
               obj.active]


