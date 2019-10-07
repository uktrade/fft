from treasuryCOA.exportcsv import EXPORT_L5_FIELD_ITERATOR_HEADERS, EXPORT_L5_HIERARCHY_ITERATOR_HEADERS, \
    l5_field_obj, l5_hierarchy_obj

EXPORT_NAC_ITERATOR_HEADERS = EXPORT_L5_HIERARCHY_ITERATOR_HEADERS + [
    'Level 6',
    'Level 6 Description'] + EXPORT_L5_FIELD_ITERATOR_HEADERS + [
                                  'Used for budget',
                                  'Budget Grouping',
                                  'Budget Category',
                                  'Commercial Category',
                                  'Operational Delivery Plan',
                                  'Prime NAC',
                                  'Active']


def _export_nac_iterator(queryset):
    yield EXPORT_NAC_ITERATOR_HEADERS

    for obj in queryset:
        yield l5_hierarchy_obj(obj.account_L5_code) + [
            obj.natural_account_code,
            obj.natural_account_code_description] + l5_field_obj(obj.account_L5_code) + [
                  obj.used_for_budget,
                  obj.expenditure_category.NAC_category.NAC_category_description if obj.expenditure_category else '-',
                  obj.expenditure_category.grouping_description if obj.expenditure_category else '-',
                  obj.commercial_category.commercial_category if obj.commercial_category else 'N/A',
                  obj.expenditure_category.op_del_category.operating_delivery_description
                  if obj.expenditure_category and obj.expenditure_category.op_del_category else 'N/A',
                  obj.expenditure_category.linked_budget_code.natural_account_code if obj.expenditure_category else '-',
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
        'Prime NAC',
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
           'Description', 'Further Description', 'Budget NAC', 'Budget NAC Description', 'Operating Delivery Plan'
           ]
    for obj in queryset:
        yield [obj.NAC_category.NAC_category_description,
               obj.grouping_description,
               obj.description,
               obj.further_description,
               obj.linked_budget_code.natural_account_code,
               obj.linked_budget_code.natural_account_code_description,
               obj.op_del_category.operating_delivery_description if obj.op_del_category else '-']


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


def _export_op_del_cat_iterator(queryset):
    yield ['Operating Delivery Plan Category']

    for obj in queryset:
        yield [obj.operating_delivery_description, ]


def _export_nac_cat_iterator(queryset):
    yield ['Budget Grouping']

    for obj in queryset:
        yield [obj.NAC_category_description, ]


def _export_programme_iterator(queryset):
    yield ['Programme Code', 'Description', 'Budget Type', 'Active']
    for obj in queryset:
        yield [obj.programme_code,
               obj.programme_description,
               obj.budget_type_fk.budget_type,
               obj.active]


def _export_historical_programme_iterator(queryset):
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
           'Oracle (DIT) Code', 'Oracle (DIT) Description', 'Active']
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
