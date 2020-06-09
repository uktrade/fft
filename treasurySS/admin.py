from django.contrib import admin

from core.admin import (
    AdminEditOnly,
    AdminImportExport,
    AdminReadOnly,
)

from treasurySS.import_csv import import_SS_class
from treasurySS.models import (
    EstimateRow,
    Segment,
    SegmentGrandParent,
    SegmentParent,
    SubSegment,
)


class SegmentAdmin(AdminReadOnly):
    list_display = ("segment_code", "segment_long_name", "segment_parent_code")


class SegmentGrandParentAdmin(AdminReadOnly):
    list_display = (
        "segment_grand_parent_code",
        "segment_grand_parent_long_name",
        "segment_department_code",
        "segment_department_long_name",
    )


class SegmentParentAdmin(AdminReadOnly):
    list_display = (
        "segment_parent_code",
        "segment_parent_long_name",
        "segment_grand_parent_code",
    )


class EstimateRowAdmin(AdminReadOnly):
    list_display = ("estimate_row_code", "estimate_row_long_name")


class SubSegmentAdmin(AdminEditOnly, AdminImportExport):
    list_display = (
        "sub_segment_code",
        "sub_segment_long_name",
        "Segment_code",
        "control_budget_detail_code",
        "dit_budget_type",
        "accounting_authority_DetailCode",
    )

    def get_readonly_fields(self, request, obj=None):
        return [
            "sub_segment_code",
            "sub_segment_long_name",
            "Segment_code",
            "control_budget_detail_code",
            "accounting_authority_DetailCode",
            "accounting_authority_code",
            "estimates_row_code",
        ]

    def get_fields(self, request, obj=None):
        return [
            "sub_segment_code",
            "sub_segment_long_name",
            "Segment_code",
            "control_budget_detail_code",
            "dit_budget_type",
            "accounting_authority_DetailCode",
            "accounting_authority_code",
            "estimates_row_code",
        ]

    @property
    def import_info(self):
        return import_SS_class


admin.site.register(Segment, SegmentAdmin)
admin.site.register(SegmentGrandParent, SegmentGrandParentAdmin)
admin.site.register(SegmentParent, SegmentParentAdmin)
admin.site.register(SubSegment, SubSegmentAdmin)
admin.site.register(EstimateRow, EstimateRowAdmin)
