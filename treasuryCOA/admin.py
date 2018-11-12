from core.admin import AdminExport, AdminImportExport, AdminreadOnly

from django.contrib import admin

from .importcsv import import_L5_class
from .models import L1Account, L2Account, L3Account, L4Account, L5Account

EXPORT_L5_ITERATOR_HEADERS = ['L0 Code', 'Accounts Code',
                              'L1 Code', 'L1 Name',
                              'L2 Code', 'L2 Name',
                              'L3 Code', 'L3 Name',
                              'L4 Code', 'L4 Name',
                              'L5 Code', 'L5 Name', 'L5 Description',
                              'Economic Budget', 'Sector', 'Estimate Column',
                              'Usage', 'Cash Indicator'
                              ]


def _export_L5_iterator(queryset):
    yield EXPORT_L5_ITERATOR_HEADERS
    for obj in queryset:
        yield [
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


# Displays extra fields in the list of cost centres
class L5AccountAdmin(AdminreadOnly, AdminImportExport):
    list_display = ('account_l5_code', 'account_l5_long_name',
                    'economic_budget_code', 'usage_code')
    list_filter = ('economic_budget_code', 'usage_code')

    @property
    def export_func(self):
        return _export_L5_iterator

    @property
    def import_info(self):
        return import_L5_class


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


# Displays extra fields in the list of cost centres
class L4AccountAdmin(AdminreadOnly, AdminExport):
    list_display = ('account_l4_code', 'account_l4_long_name', 'account_l3')

    @property
    def export_func(self):
        return _export_L4_iterator


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


class L3AccountAdmin(AdminreadOnly, AdminExport):
    list_display = ('account_l3_code', 'account_l3_long_name', 'account_l2')

    @property
    def export_func(self):
        return _export_L3_iterator


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


class L2AccountAdmin(AdminreadOnly, AdminExport):
    list_display = ('account_l2_code', 'account_l2_long_name', 'account_l1')

    @property
    def export_func(self):
        return _export_L2_iterator


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


class L1AccountAdmin(AdminreadOnly, AdminExport):
    list_display = ('account_l1_code', 'account_l1_long_name')

    @property
    def export_func(self):
        return _export_L1_iterator


# Register your models here.
admin.site.register(L1Account, L1AccountAdmin)
admin.site.register(L2Account, L2AccountAdmin)
admin.site.register(L3Account, L3AccountAdmin)
admin.site.register(L4Account, L4AccountAdmin)
admin.site.register(L5Account, L5AccountAdmin)
