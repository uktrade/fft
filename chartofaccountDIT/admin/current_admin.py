from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from chartofaccountDIT.exportcsv import (
    _export_comm_cat_iterator,
    _export_exp_cat_iterator,
    _export_fco_mapping_iterator,
    _export_inter_entity_iterator,
    _export_inter_entity_l1_iterator,
    _export_nac_cat_iterator,
    _export_nac_iterator,
    _export_op_del_cat_iterator,
    _export_programme_iterator,
)
from chartofaccountDIT.import_csv import (
    import_analysis1_class,
    import_analysis2_class,
    import_comm_cat_class,
    import_expenditure_category_class,
    import_fco_mapping_class,
    import_inter_entity_class,
    import_NAC_category_class,
    import_NAC_class,
    import_NAC_DIT_class,
    import_op_del_category_class,
    import_prog_class,
    import_project_class,
)
from chartofaccountDIT.models import (
    Analysis1,
    Analysis2,
    BudgetType,
    CommercialCategory,
    ExpenditureCategory,
    FCOMapping,
    InterEntity,
    InterEntityL1,
    NACCategory,
    NaturalCode,
    OperatingDeliveryCategory,
    ProgrammeCode,
    ProjectCode,
)
from core.admin import (
    AdminActiveField,
    AdminExport,
    AdminImportExport,
    AdminImportExtraExport,
)
from core.utils.export_helpers import generic_table_iterator


class NaturalCodeAdmin(AdminActiveField, AdminImportExtraExport):
    # Define an extra import button, for the DIT specific fields
    change_list_template = "admin/m_import_changelist.html"

    list_display = (
        "natural_account_code",
        "natural_account_code_description",
        "active",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            fields = [
                "natural_account_code",
                "natural_account_code_description",
                "created",
                "updated",
            ]

            if not request.user.is_superuser:
                fields.append("account_L5_code")

            return fields
        else:
            return ["created", "updated"]

    def get_fields(self, request, obj=None):
        return [
            "natural_account_code",
            "natural_account_code_description",
            "account_L5_code",
            "expenditure_category",
            "account_L5_code_upload",
            "commercial_category",
            "used_for_budget",
            "active",
            "created",
            "updated",
        ]

    search_fields = ["natural_account_code", "natural_account_code_description"]
    list_filter = (
        "active",
        "used_for_budget",
        ("expenditure_category__NAC_category", RelatedDropdownFilter),
        ("expenditure_category", RelatedDropdownFilter),
    )

    queryset_all = NaturalCode.objects.select_related(
        "expenditure_category",
        "expenditure_category__NAC_category",
        "expenditure_category__linked_budget_code",
        "commercial_category",
        "account_L5_code",
        "account_L5_code__account_l4",
        "account_L5_code__account_l4__account_l3",
        "account_L5_code__account_l4__account_l3__account_l2",
        "account_L5_code__account_l4__account_l3__account_l2__account_l1",
    )

    @property
    def export_func(self):
        return _export_nac_iterator

    @property
    def import_info(self):
        return import_NAC_class

    @property
    def import_extra_info(self):
        return import_NAC_DIT_class


class Analysis1Admin(AdminActiveField, AdminImportExport):
    search_fields = ["analysis1_description", "analysis1_code"]
    list_display = ("analysis1_code", "analysis1_description", "active")

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "analysis1_code",
                "created",
                "updated",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "analysis1_code",
                "analysis1_description",
                "supplier",
                "pc_reference",
                "active",
                "created",
                "updated",
            ]
        else:
            return [
                "analysis1_code",
                "analysis1_description",
                "supplier",
                "pc_reference",
                "active",
            ]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_analysis1_class


class Analysis2Admin(AdminActiveField, AdminImportExport):
    search_fields = ["analysis2_description", "analysis2_code"]
    list_display = ("analysis2_code", "analysis2_description", "active")

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "analysis2_code",
                "created",
                "updated",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "analysis2_code",
                "analysis2_description",
                "active",
                "created",
                "updated",
            ]
        else:
            return ["analysis2_code", "analysis2_description", "active"]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_analysis2_class


class ExpenditureCategoryAdmin(AdminImportExport):
    search_fields = ["grouping_description", "description"]
    list_display = [
        "grouping_description",
        "description",
        "NAC_category",
        "op_del_category",
        "linked_budget_code",
    ]
    list_filter = ("NAC_category",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "linked_budget_code":
            kwargs["queryset"] = NaturalCode.objects.filter(used_for_budget=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    def get_fields(self, request, obj=None):
        if obj:
            return [
                "grouping_description",
                "description",
                "further_description",
                "linked_budget_code",
                "NAC_category",
                "op_del_category",
                "created",
                "updated",
            ]
        else:
            return [
                "grouping_description",
                "description",
                "further_description",
                "linked_budget_code",
                "NAC_category",
            ]

    @property
    def export_func(self):
        return _export_exp_cat_iterator

    @property
    def import_info(self):
        return import_expenditure_category_class


class CommercialCategoryAdmin(AdminImportExport):
    search_fields = ["commercial_category", "description"]
    list_display = ["commercial_category", "description", "commercial_category"]

    @property
    def export_func(self):
        return _export_comm_cat_iterator

    @property
    def import_info(self):
        return import_comm_cat_class


class NACCategoryAdmin(AdminImportExport):
    search_fields = ["NAC_category_description"]
    list_display = ["NAC_category_description"]

    @property
    def export_func(self):
        return _export_nac_cat_iterator

    @property
    def import_info(self):
        return import_NAC_category_class


class ProgrammeAdmin(AdminActiveField, AdminImportExtraExport):
    change_list_template = "admin/m_import_changelist.html"

    list_display = (
        "programme_code",
        "programme_description",
        "budget_type",
        "active",
        "created",
        "updated",
    )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ["created", "updated"]
        elif request.user.groups.filter(name="Finance Administrator"):
            if obj:
                return [
                    "programme_code",
                    "created",
                    "updated",
                ]  # don't allow to edit the code
            else:
                return ["created", "updated"]
        else:
            return self.get_fields(request, obj)

    def get_fields(self, request, obj=None):
        return [
            "programme_code",
            "programme_description",
            "budget_type",
            "active",
            "created",
            "updated",
        ]

    search_fields = ["programme_code", "programme_description"]
    list_filter = ["budget_type", "active"]

    @property
    def export_func(self):
        return _export_programme_iterator

    @property
    def import_info(self):
        return import_prog_class


class InterEntityL1Admin(AdminActiveField, AdminExport):
    search_fields = ["l1_value", "l1_description"]

    @property
    def export_func(self):
        return _export_inter_entity_l1_iterator


class InterEntityAdmin(AdminActiveField, AdminImportExport):
    list_display = ("l2_value", "l2_description", "l1_value", "active")
    search_fields = ["l2_value", "l2_description"]
    list_filter = ("active", "l1_value")

    @property
    def export_func(self):
        return _export_inter_entity_iterator

    @property
    def import_info(self):
        return import_inter_entity_class


class ProjectCodeAdmin(AdminActiveField, AdminImportExport):
    search_fields = ["project_description", "project_code"]
    list_display = ("project_code", "project_description", "active")

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "project_code",
                "created",
                "updated",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "project_code",
                "project_description",
                "active",
                "created",
                "updated",
            ]
        else:
            return ["project_code", "project_description", "active"]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_project_class


class FCOMappingAdmin(AdminActiveField, AdminImportExport):
    search_fields = ["fco_code", "fco_description"]
    list_display = ("fco_code", "fco_description", "active")

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "fco_code",
                "fco_description",
                "created",
                "updated",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "fco_code",
                "fco_description",
                "account_L6_code_fk",
                "active",
                "created",
                "updated",
            ]
        else:
            return ["fco_code", "fco_description", "account_L6_code_fk", "active"]

    @property
    def export_func(self):
        return _export_fco_mapping_iterator

    @property
    def import_info(self):
        return import_fco_mapping_class


class OpDelCategoryAdmin(AdminImportExport):
    search_fields = ["operating_delivery_description"]
    list_display = ["operating_delivery_description"]

    @property
    def export_func(self):
        return _export_op_del_cat_iterator

    @property
    def import_info(self):
        return import_op_del_category_class


class BudgetTypeAdmin(AdminImportExport):
    list_display = (
        "budget_type_key",
        "budget_type",
    )

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "budget_type_key",
                "budget_type",
                "budget_type_display",
                "created",
                "updated",
            ]  # don't allow to edit the code
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return [
                "budget_type_key",
                "budget_type",
                "budget_type_display",
                "budget_type_display_order",
                "budget_type_edit_display_order",
                "created",
                "updated",
            ]
        else:
            return [
                "budget_type_key",
                "budget_type",
                "budget_type_display",
                "budget_type_display_order",
                "budget_type_edit_display_order",
            ]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_project_class


admin.site.register(Analysis1, Analysis1Admin)
admin.site.register(Analysis2, Analysis2Admin)
admin.site.register(NaturalCode, NaturalCodeAdmin)
admin.site.register(ExpenditureCategory, ExpenditureCategoryAdmin)
admin.site.register(NACCategory, NACCategoryAdmin)
admin.site.register(CommercialCategory, CommercialCategoryAdmin)
admin.site.register(ProgrammeCode, ProgrammeAdmin)
admin.site.register(InterEntityL1, InterEntityL1Admin)
admin.site.register(InterEntity, InterEntityAdmin)
admin.site.register(ProjectCode, ProjectCodeAdmin)
admin.site.register(FCOMapping, FCOMappingAdmin)
admin.site.register(OperatingDeliveryCategory, OpDelCategoryAdmin)
admin.site.register(BudgetType, BudgetTypeAdmin)
