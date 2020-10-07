from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from chartofaccountDIT.exportcsv import (
    _export_historical_comm_cat_iterator,
    _export_historical_exp_cat_iterator,
    _export_historical_fco_mapping_iterator,
    _export_historical_inter_entity_iterator,
    _export_historical_nac_iterator,
    _export_programme_iterator,
)
from chartofaccountDIT.models import (
    ArchivedAnalysis1,
    ArchivedAnalysis2,
    ArchivedCommercialCategory,
    ArchivedExpenditureCategory,
    ArchivedFCOMapping,
    ArchivedInterEntity,
    ArchivedNaturalCode,
    ArchivedProgrammeCode,
    ArchivedProjectCode,
)

from core.admin import (
    AdminArchived,
    AdminExport,
    AdminReadOnly,
)
from core.utils.export_helpers import generic_table_iterator


class ArchivedNaturalCodeAdmin(AdminArchived, AdminExport):
    list_display = (
        "natural_account_code",
        "natural_account_code_description",
        "active",
        "financial_year",
    )

    fields = [
        "financial_year",
        "natural_account_code",
        "natural_account_code_description",
        "account_L5_code",
        "expenditure_category",
        "commercial_category",
        "used_for_budget",
        "active",
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "natural_account_code",
                "natural_account_code_description",
                "account_L5_code",
                "created",
                "updated",
            ]
        else:
            return ["created", "updated", "archived"]

    search_fields = ["natural_account_code", "natural_account_code_description"]
    list_filter = (
        "active",
        "used_for_budget",
        ("expenditure_category__NAC_category", RelatedDropdownFilter),
        ("expenditure_category", RelatedDropdownFilter),
        ("financial_year", RelatedDropdownFilter),
    )

    @property
    def export_func(self):
        return _export_historical_nac_iterator


class ArchivedAnalysis1Admin(AdminArchived, AdminExport):
    search_fields = ["analysis1_description", "analysis1_code"]
    list_display = (
        "analysis1_code",
        "analysis1_description",
        "active",
        "financial_year",
    )
    list_filter = ("active", ("financial_year", RelatedDropdownFilter))

    def get_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "analysis1_code",
                "analysis1_description",
                "supplier",
                "pc_reference",
                "active",
                "archived",
            ]
        else:
            return [
                "financial_year",
                "analysis1_code",
                "analysis1_description",
                "supplier",
                "pc_reference",
            ]

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "analysis1_code",
                "created",
                "updated",
                "archived",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated", "archived"]

    @property
    def export_func(self):
        return generic_table_iterator


class ArchivedAnalysis2Admin(AdminArchived, AdminExport):
    search_fields = ["analysis2_description", "analysis2_code"]
    list_display = (
        "analysis2_code",
        "analysis2_description",
        "active",
        "financial_year",
    )
    list_filter = ("active", ("financial_year", RelatedDropdownFilter))
    fields = ("financial_year", "analysis2_code", "analysis2_description", "active")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "analysis2_code",
                "created",
                "updated",
                "archived",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated", "archived"]

    @property
    def export_func(self):
        return generic_table_iterator


class ArchivedExpenditureCategoryAdmin(AdminArchived, AdminExport):
    search_fields = ["grouping_description", "description"]
    list_display = [
        "grouping_description",
        "description",
        "NAC_category_description",
        "linked_budget_code",
        "financial_year",
    ]
    list_filter = (
        "NAC_category_description",
        ("financial_year", RelatedDropdownFilter),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "grouping_description",
                "NAC_category_description",
                "created",
                "updated",
                "archived",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated", "archived"]

    fields = (
        "financial_year",
        "grouping_description",
        "description",
        "further_description",
        "linked_budget_code",
        "linked_budget_code_description",
        "NAC_category_description",
        "archived",
    )

    @property
    def export_func(self):
        return _export_historical_exp_cat_iterator


class ArchivedCommercialCategoryAdmin(AdminReadOnly, AdminExport):
    search_fields = ["commercial_category", "description"]
    list_display = [
        "commercial_category",
        "description",
        "financial_year",
    ]
    list_filter = ("active", ("financial_year", RelatedDropdownFilter))

    fields = (
        "financial_year",
        "commercial_category",
        "description",
        "active",
        "archived",
    )

    @property
    def export_func(self):
        return _export_historical_comm_cat_iterator


class ArchivedProgrammeAdmin(AdminArchived, AdminExport):
    list_display = (
        "programme_code",
        "programme_description",
        "budget_type",
        "active",
        "financial_year",
    )
    search_fields = ["programme_code", "programme_description"]
    list_filter = ["budget_type", "active", ("financial_year", RelatedDropdownFilter)]
    fields = (
        "financial_year",
        "programme_code",
        "programme_description",
        "budget_type",
        "active",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "programme_code",
                "budget_type",
                "created",
                "archived",
                "updated",
            ]
        else:
            return ["created", "archived", "updated"]

    def get_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "programme_code",
                "programme_description",
                "budget_type",
                "active",
                "created",
                "updated",
            ]
        else:
            return [
                "financial_year",
                "programme_code",
                "programme_description",
                "budget_type",
                "active",
            ]

    @property
    def export_func(self):
        return _export_programme_iterator


class ArchivedInterEntityAdmin(AdminReadOnly, AdminExport):
    list_display = ("l2_value", "l2_description", "l1_value", "active")
    search_fields = ["l2_value", "l2_description"]
    list_filter = ["active", ("financial_year", RelatedDropdownFilter)]
    fields = (
        "l2_value",
        "l2_description",
        "l1_value",
        "l1_description",
        "active",
        "financial_year",
    )

    @property
    def export_func(self):
        return _export_historical_inter_entity_iterator


class ArchivedProjectCodeAdmin(AdminArchived, AdminExport):
    search_fields = ["project_description", "project_code"]
    list_display = ("project_code", "project_description", "active", "financial_year")
    list_filter = ["active", ("financial_year", RelatedDropdownFilter)]
    fields = ("financial_year", "project_code", "project_description", "active")

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "project_code",
                "financial_year",
                "created",
                "updated",
            ]
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "financial_year",
                "project_code",
                "project_description",
                "active",
                "created",
                "updated",
            ]
        else:
            return ["financial_year", "project_code", "project_description", "active"]

    @property
    def export_func(self):
        return generic_table_iterator


class ArchivedFCOMappingAdmin(AdminReadOnly, AdminExport):
    search_fields = ["fco_code", "fco_description"]
    list_display = ("fco_code", "fco_description", "active", "financial_year")
    list_filter = ["active", ("financial_year", RelatedDropdownFilter)]
    fields = (
        "financial_year",
        "fco_code",
        "fco_description",
        "account_L6_code",
        "account_L6_description",
        "nac_category_description",
        "budget_description",
        "economic_budget_code",
        "active",
    )

    @property
    def export_func(self):
        return _export_historical_fco_mapping_iterator


admin.site.register(ArchivedAnalysis1, ArchivedAnalysis1Admin)
admin.site.register(ArchivedAnalysis2, ArchivedAnalysis2Admin)
admin.site.register(ArchivedExpenditureCategory, ArchivedExpenditureCategoryAdmin)
admin.site.register(ArchivedCommercialCategory, ArchivedCommercialCategoryAdmin)
admin.site.register(ArchivedNaturalCode, ArchivedNaturalCodeAdmin)
admin.site.register(ArchivedProgrammeCode, ArchivedProgrammeAdmin)
admin.site.register(ArchivedInterEntity, ArchivedInterEntityAdmin)
admin.site.register(ArchivedProjectCode, ArchivedProjectCodeAdmin)
admin.site.register(ArchivedFCOMapping, ArchivedFCOMappingAdmin)
