from django.contrib import (
    admin,
    messages,
)
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from core.admin import (
    AdminEditOnly,
    AdminImportExport,
    AdminReadOnly,
)

from treasurySS.export_csv import _export_sub_segment_iterator
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
    search_fields = [
        "sub_segment_code",
        "sub_segment_long_name",
        "Segment_code__segment_code",
        "Segment_code__segment_long_name",
        "control_budget_detail_code",
        "dit_budget_type__budget_type",
        "accounting_authority_DetailCode",
    ]

    list_filter = (
        "control_budget_detail_code",
        "dit_budget_type",
    )

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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super(SubSegmentAdmin, self).change_view(
                request,
                object_id,
                form_url,
                extra_context
            )
        except IntegrityError as err:
            messages.error(request, err)
            return HttpResponseRedirect(request.path)

    @property
    def import_info(self):
        return import_SS_class

    @property
    def export_func(self):
        return _export_sub_segment_iterator


admin.site.register(Segment, SegmentAdmin)
admin.site.register(SegmentGrandParent, SegmentGrandParentAdmin)
admin.site.register(SegmentParent, SegmentParentAdmin)
admin.site.register(SubSegment, SubSegmentAdmin)
admin.site.register(EstimateRow, EstimateRowAdmin)
