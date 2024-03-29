from django.contrib import admin

from core.admin import AdminExport, AdminImportExport, AdminReadOnly
from treasuryCOA.export_csv import (
    _export_historic_L5_iterator,
    _export_L1_iterator,
    _export_L2_iterator,
    _export_L3_iterator,
    _export_L4_iterator,
    _export_L5_iterator,
)
from treasuryCOA.import_csv import import_L5_class
from treasuryCOA.models import (
    HistoricL5Account,
    L1Account,
    L2Account,
    L3Account,
    L4Account,
    L5Account,
)


class L5AccountAdmin(AdminReadOnly, AdminImportExport):
    list_display = (
        "account_l5_code",
        "account_l5_long_name",
        "economic_budget_code",
        "usage_code",
    )
    list_filter = ("economic_budget_code", "usage_code")

    @property
    def export_func(self):
        return _export_L5_iterator

    @property
    def import_info(self):
        return import_L5_class


class L4AccountAdmin(AdminReadOnly, AdminExport):
    list_display = ("account_l4_code", "account_l4_long_name", "account_l3")

    @property
    def export_func(self):
        return _export_L4_iterator


class L3AccountAdmin(AdminReadOnly, AdminExport):
    list_display = ("account_l3_code", "account_l3_long_name", "account_l2")

    @property
    def export_func(self):
        return _export_L3_iterator


class L2AccountAdmin(AdminReadOnly, AdminExport):
    list_display = ("account_l2_code", "account_l2_long_name", "account_l1")

    @property
    def export_func(self):
        return _export_L2_iterator


class L1AccountAdmin(AdminReadOnly, AdminExport):
    list_display = ("account_l1_code", "account_l1_long_name")

    @property
    def export_func(self):
        return _export_L1_iterator


class HistoricL5AccountAdmin(AdminReadOnly, AdminExport):
    list_display = (
        "financial_year",
        "account_l5_code",
        "account_l5_long_name",
        "economic_budget_code",
        "usage_code",
    )
    list_filter = ("economic_budget_code", "usage_code")

    @property
    def export_func(self):
        return _export_historic_L5_iterator


# Register your models here.
admin.site.register(L1Account, L1AccountAdmin)
admin.site.register(L2Account, L2AccountAdmin)
admin.site.register(L3Account, L3AccountAdmin)
admin.site.register(L4Account, L4AccountAdmin)
admin.site.register(L5Account, L5AccountAdmin)
admin.site.register(HistoricL5Account, HistoricL5AccountAdmin)
