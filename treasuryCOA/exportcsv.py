EXPORT_L5_ITERATOR_HEADERS = ['L0 Code', 'Accounts Code',
                              'L1 Code', 'L1 Name',
                              'L2 Code', 'L2 Name',
                              'L3 Code', 'L3 Name',
                              'L4 Code', 'L4 Name',
                              'L5 Code', 'L5 Name', 'L5 Description',
                              'Economic Budget', 'Sector', 'Estimate Column',
                              'Usage', 'Cash Indicator'
                              ]


def full_l5_obj(obj):
    if obj:
        return [obj.account_l4.account_l3.account_l2.account_l1.account_l0_code,
                obj.account_l4.account_l3.account_l2.account_l1.account_code,
                obj.account_l4.account_l3.account_l2.account_l1.account_l1_code,
                obj.account_l4.account_l3.account_l2.account_l1.account_l1_long_name,
                obj.account_l4.account_l3.account_l2.account_l2_code,
                obj.account_l4.account_l3.account_l2.account_l2_long_name,
                obj.account_l4.account_l3.account_l3_code,
                obj.account_l4.account_l3.account_l3_long_name,
                obj.account_l4.account_l4_code,
                obj.account_l4.account_l4_long_name,
                obj.account_l5_code,
                obj.account_l5_long_name,
                obj.account_l5_description,
                obj.economic_budget_code,
                obj.sector_code,
                obj.estimates_column_code,
                obj.usage_code,
                obj.cash_indicator_code]
    return ['-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-',
            '-']


def _export_L5_iterator(queryset):
    yield EXPORT_L5_ITERATOR_HEADERS
    for obj in queryset:
        yield full_l5_obj(obj)


# L4 Account
EXPORT_L4_ITERATOR_HEADERS = ['L0 Code', 'Accounts Code',
                              'L1 Code', 'L1 Name',
                              'L2 Code', 'L2 Name',
                              'L3 Code', 'L3 Name',
                              'L4 Code', 'L4 Name'
                              ]


def _export_L4_iterator(queryset):
    yield EXPORT_L4_ITERATOR_HEADERS
    for obj in queryset:
        yield [
            obj.account_l3.account_l2.account_l1.account_l0_code,
            obj.account_l3.account_l2.account_l1.account_code,
            obj.account_l3.account_l2.account_l1.account_l1_code,
            obj.account_l3.account_l2.account_l1.account_l1_long_name,
            obj.account_l3.account_l2.account_l2_code,
            obj.account_l3.account_l2.account_l2_long_name,
            obj.account_l3.account_l3_code,
            obj.account_l3.account_l3_long_name,
            obj.account_l4_code,
            obj.account_l4_long_name
        ]


#  L3 Account
EXPORT_L3_ITERATOR_HEADERS = ['L0 Code', 'Accounts Code',
                              'L1 Code', 'L1 Name',
                              'L2 Code', 'L2 Name',
                              'L3 Code', 'L3 Name'
                              ]


def _export_L3_iterator(queryset):
    yield EXPORT_L3_ITERATOR_HEADERS
    for obj in queryset:
        yield [
            obj.account_l2.account_l1.account_l0_code,
            obj.account_l2.account_l1.account_code,
            obj.account_l2.account_l1.account_l1_code,
            obj.account_l2.account_l1.account_l1_long_name,
            obj.account_l2.account_l2_code,
            obj.account_l2.account_l2_long_name,
            obj.account_l3_code,
            obj.account_l3_long_name
        ]


#  L2 Account
EXPORT_L2_ITERATOR_HEADERS = ['L0 Code', 'Accounts Code',
                              'L1 Code', 'L1 Name',
                              'L2 Code', 'L2 Name',
                              ]


def _export_L2_iterator(queryset):
    yield EXPORT_L2_ITERATOR_HEADERS
    for obj in queryset:
        yield [
            obj.account_l1.account_l0_code,
            obj.account_l1.account_code,
            obj.account_l1.account_l1_code,
            obj.account_l1.account_l1_long_name,
            obj.account_l2_code,
            obj.account_l2_long_name
        ]


# L1 Account
EXPORT_L1_ITERATOR_HEADERS = ['L0 Code', 'Accounts Code',
                              'L1 Code', 'L1 Name'
                              ]


def _export_L1_iterator(queryset):
    yield EXPORT_L1_ITERATOR_HEADERS
    for obj in queryset:
        yield [
            obj.account_l0_code,
            obj.account_code,
            obj.account_l1_code,
            obj.account_l1_long_name
        ]


def _export_historic_L5_iterator(queryset):
    yield [
        'account l5 code',
        'account l5 long name',
        'account l5 description',
        'economic budget code',
        'sector code',
        'estimates column code',
        'usage code',
        'cash indicator code',
        'account l4 code',
        'account l4 long name',
        'account l3 code',
        'account l3 long name',
        'account l2 code',
        'account l2 long name',
        'account l1 code',
        'account l1 long name',
        'accounts code',
        'account l0 code',
        'financial year',
        'archived']

    for obj in queryset:
        yield [
            obj.account_l5_code,
            obj.account_l5_long_name,
            obj.account_l5_description,
            obj.economic_budget_code,
            obj.sector_code,
            obj.estimates_column_code,
            obj.usage_code,
            obj.cash_indicator_code,
            obj.account_l4_code,
            obj.account_l4_long_name,
            obj.account_l3_code,
            obj.account_l3_long_name,
            obj.account_l2_code,
            obj.account_l2_long_name,
            obj.account_l1_code,
            obj.account_l1_long_name,
            obj.account_code,
            obj.account_l0_code,
            obj.financial_year.financial_year_display,
            obj.archived
        ]
