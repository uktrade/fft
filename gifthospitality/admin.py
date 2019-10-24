from core.admin import AdminActiveField, AdminImportExport
from core.exportutils import generic_table_iterator

from django.contrib import admin

from gifthospitality.export_csv import _export_gh_iterator
from gifthospitality.import_csv import (
    import_gh_category_class,
    import_gh_class,
    import_gh_classification_class,
    import_gh_company_class,
)
from .models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
)


class GiftAndHospitalityCompanyAdmin(AdminActiveField, AdminImportExport):
    list_display = ("gif_hospitality_company", "sequence_no", "active")
    list_editable = ("sequence_no",)
    search_fields = ["gif_hospitality_company"]

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_company_class


class GiftAndHospitalityCategoryAdmin(AdminActiveField, AdminImportExport):
    list_display = ("gif_hospitality_category", "sequence_no", "active")
    list_editable = ("sequence_no",)
    search_fields = ["gif_hospitality_category"]

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_category_class


class GiftAndHospitalityClassificationAdmin(AdminActiveField, AdminImportExport):
    list_display = (
        "gift_type",
        "gif_hospitality_classification",
        "sequence_no",
        "active",
    )
    list_editable = ("sequence_no",)
    search_fields = ["gift_type", "gif_hospitality_classification"]

    def get_readonly_fields(self, request, obj=None):
        return ["created", "updated"]

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_gh_classification_class


class GiftAndHospitalityAdmin(AdminImportExport):
    def gift_or_hospitality(
        self, instance
    ):  # required to display the field from a foreign key
        return instance.classification_fk.gift_type

    gift_or_hospitality.admin_order_field = "classification_fk__gift_type"

    list_display = (
        "id",
        "gift_or_hospitality",
        "category_fk",
        "classification_fk",
        "group_name",
        "date_offered",
        "venue",
        "reason",
        "value",
        "rep",
        "grade_fk",
        "offer",
        "company_rep",
        "company",
        "action_taken",
        "entered_date_stamp",
        "entered_by",
    )
    search_fields = ["id", "rep", "entered_by"]

    list_filter = ("classification_fk__gift_type", "offer", "action_taken")

    def get_fields(self, request, obj=None):
        return [
            "gift_or_hospitality",
            "category_fk",
            "classification_fk",
            "group_name",
            "date_offered",
            "venue",
            "reason",
            "value",
            "rep",
            "grade_fk",
            "offer",
            "company_rep",
            "company",
            "action_taken",
            "entered_by",
            "entered_date_stamp",
        ]

    def get_readonly_fields(self, request, obj=None):
        return ["gift_or_hospitality", "entered_by", "entered_date_stamp"]

    # Don't allow add
    def has_add_permission(self, request):
        return False

    @property
    def export_func(self):
        return _export_gh_iterator

    @property
    def import_info(self):
        return import_gh_class


admin.site.register(GiftAndHospitality, GiftAndHospitalityAdmin)
admin.site.register(GiftAndHospitalityCompany, GiftAndHospitalityCompanyAdmin)
admin.site.register(GiftAndHospitalityCategory, GiftAndHospitalityCategoryAdmin)
admin.site.register(
    GiftAndHospitalityClassification, GiftAndHospitalityClassificationAdmin
)
