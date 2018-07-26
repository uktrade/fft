from django.contrib import admin
from core.exportutils import export_to_csv, export_to_excel
from core.myutils import AdminreadOnly

from .models import L1Account, L2Account, L3Account, L4Account, L5Account

EXPORT_L5_ITERATOR_HEADERS=['L0 Code', 'Accounts Code',
                            'L1 Code', 'L1 Name',
                            'L2 Code', 'L2 Name',
                            'L3 Code', 'L3 Name',
                            'L4 Code', 'L4 Name',
                            'L5 Code','L5 Name', 'L5 Description',
                            'Economic Budget', 'Sector','Estimate Column',
                            'Usage', 'Cash Indicator'
                            ]

def _export_L5_iterator(queryset):
    yield EXPORT_L5_ITERATOR_HEADERS
    for obj in queryset:
        yield[
            obj.account_l4.account_l3.account_l2.account_l1.account_l0_code,
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
            obj.cash_indicator_code
        ]




def export_L5_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_L5_iterator))

def export_L5_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_L5_iterator))

export_L5_xlsx.short_description = u"Export to xslx"
export_L5_csv.short_description = u"Export to csv"

# Displays extra fields in the list of cost centres
class L5AccountAdmin(AdminreadOnly):
    list_display = ('account_l5_code', 'account_l5_long_name',  'economic_budget_code', 'usage_code')
    list_filter = ('economic_budget_code', 'usage_code')


    # directorate.admin_order_field = 'directorate__directorate_name'  # use __ to define a table field relationship
    # group.admin_order_field = 'directorate__group__group_name'  # use __ to define a table field relationship
    #
    # search_fields = ['cost_centre_code']
    # list_filter = ['active','directorate__directorate_name','directorate__group__group_name']
    actions = [export_L5_csv, export_L5_xlsx] # new action to export to csv and xlsx


#################################### L4 Account ########################################

EXPORT_L4_ITERATOR_HEADERS=['L0 Code', 'Accounts Code',
                            'L1 Code', 'L1 Name',
                            'L2 Code', 'L2 Name',
                            'L3 Code', 'L3 Name',
                            'L4 Code', 'L4 Name'
                            ]

def _export_L4_iterator(queryset):
    yield EXPORT_L4_ITERATOR_HEADERS
    for obj in queryset:
        yield[
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


def export_L4_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_L4_iterator))

def export_L4_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_L4_iterator))

export_L4_xlsx.short_description = u"Export to xslx"
export_L4_csv.short_description = u"Export to csv"


# Displays extra fields in the list of cost centres
class L4AccountAdmin(AdminreadOnly):
    list_display = ('account_l4_code', 'account_l4_long_name',  'account_l3')
    actions = [export_L4_csv, export_L4_xlsx] # new action to export to csv and xlsx


#################################### L3 Account ########################################

EXPORT_L3_ITERATOR_HEADERS=['L0 Code', 'Accounts Code',
                            'L1 Code', 'L1 Name',
                            'L2 Code', 'L2 Name',
                            'L3 Code', 'L3 Name'
                             ]

def _export_L3_iterator(queryset):
    yield EXPORT_L3_ITERATOR_HEADERS
    for obj in queryset:
        yield[
            obj.account_l2.account_l1.account_l0_code,
            obj.account_l2.account_l1.account_code,
            obj.account_l2.account_l1.account_l1_code,
            obj.account_l2.account_l1.account_l1_long_name,
            obj.account_l2.account_l2_code,
            obj.account_l2.account_l2_long_name,
            obj.account_l3_code,
            obj.account_l3_long_name
        ]


def export_L3_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_L3_iterator))

def export_L3_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_L3_iterator))

export_L3_xlsx.short_description = u"Export to xslx"
export_L3_csv.short_description = u"Export to csv"


class L3AccountAdmin(AdminreadOnly):
    list_display = ('account_l3_code', 'account_l3_long_name',  'account_l2')
    actions = [export_L3_csv, export_L3_xlsx] # new action to export to csv and xlsx

#################################### L2 Account ########################################

EXPORT_L2_ITERATOR_HEADERS=['L0 Code', 'Accounts Code',
                            'L1 Code', 'L1 Name',
                            'L2 Code', 'L2 Name',
                             ]

def _export_L2_iterator(queryset):
    yield EXPORT_L2_ITERATOR_HEADERS
    for obj in queryset:
        yield[
            obj.account_l1.account_l0_code,
            obj.account_l1.account_code,
            obj.account_l1.account_l1_code,
            obj.account_l1.account_l1_long_name,
            obj.account_l2_code,
            obj.account_l2_long_name
        ]


def export_L2_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_L2_iterator))

def export_L2_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_L2_iterator))

export_L2_xlsx.short_description = u"Export to xslx"
export_L2_csv.short_description = u"Export to csv"


class L2AccountAdmin(AdminreadOnly):
    list_display = ('account_l2_code', 'account_l2_long_name',  'account_l1')
    actions = [export_L2_csv, export_L2_xlsx] # new action to export to csv and xlsx


#################################### L1 Account ########################################

EXPORT_L1_ITERATOR_HEADERS=['L0 Code', 'Accounts Code',
                            'L1 Code', 'L1 Name'
                             ]

def _export_L1_iterator(queryset):
    yield EXPORT_L1_ITERATOR_HEADERS
    for obj in queryset:
        yield[
            obj.account_l0_code,
            obj.account_code,
            obj.account_l1_code,
            obj.account_l1_long_name
         ]


def export_L1_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_L1_iterator))

def export_L1_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_L1_iterator))

export_L1_xlsx.short_description = u"Export to xslx"
export_L1_csv.short_description = u"Export to csv"


class L1AccountAdmin(AdminreadOnly):
    list_display = ('account_l1_code', 'account_l1_long_name')
    actions = [export_L1_csv, export_L1_xlsx] # new action to export to csv and xlsx




# Register your models here.
admin.site.register(L1Account, L1AccountAdmin)
admin.site.register(L2Account, L2AccountAdmin)
admin.site.register(L3Account, L3AccountAdmin)
admin.site.register(L4Account, L4AccountAdmin)
admin.site.register(L5Account, L5AccountAdmin)


