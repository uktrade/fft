from django.contrib import admin

from core.admin import AdminActiveField, AdminImportExport
from core.exportutils import generic_table_iterator

from gifthospitality.export_csv import _export_gh_iterator
from gifthospitality.import_csv import (
    import_gh_category_class,
    import_gh_class,
    import_gh_classification_class,
    import_gh_company_class,
    import_grade_class,
)
from gifthospitality.models import (
    GiftAndHospitality,
    GiftAndHospitalityCategory,
    GiftAndHospitalityClassification,
    GiftAndHospitalityCompany,
    Grade,
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


def _export_grade_iterator(queryset):
    yield ["Grade", "Grade Description"]
    for obj in queryset:
        yield [obj.grade, obj.gradedescription]


class GradeAdmin(AdminImportExport):
    list_display = ("grade", "gradedescription")

    @property
    def export_func(self):
        return _export_grade_iterator

    @property
    def import_info(self):
        return import_grade_class


class GiftAndHospitalityAdmin(AdminImportExport):
    def gift_or_hospitality(
        self, instance
    ):  # required to display the field from a foreign key
        return instance.classification.gift_type

    gift_or_hospitality.admin_order_field = "classification__gift_type"

    list_display = (
        "id",
        "gift_or_hospitality",
        "category",
        "classification",
        "group_name",
        "date_offered",
        "venue",
        "reason",
        "value",
        "group",
        "rep",
        "grade",
        "offer",
        "company_rep",
        "company",
        "action_taken",
        "entered_date_stamp",
        "entered_by",
    )
    search_fields = ["id", "rep", "group", "entered_by"]

    list_filter = ("classification__gift_type", "offer", "action_taken")

    def get_fields(self, request, obj=None):
        return [
            "gift_or_hospitality",
            "category",
            "classification",
            "group_name",
            "date_offered",
            "venue",
            "reason",
            "value",
            "group",
            "rep",
            "grade",
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
admin.site.register(Grade, GradeAdmin)
