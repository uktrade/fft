from core.admin import AdminExport, AdminImportExport, AdminreadOnly

from django.contrib import admin

from .importcsv import import_SS_class
from .models import EstimateRow, Segment, SegmentGrandParent, SegmentParent, SubSegment


class SegmentAdmin(AdminreadOnly):
    list_display = ('segment_code', 'segment_long_name', 'segment_parent_code')


class SegmentGrandParentAdmin(AdminreadOnly):
    list_display = ('segment_grand_parent_code', 'segment_grand_parent_long_name',
                    'segment_department_code', 'segment_department_long_name')


class SegmentParentAdmin(AdminreadOnly):
    list_display = ('segment_parent_code', 'segment_parent_long_name',
                    'segment_grand_parent_code')


class EstimateRowAdmin(AdminreadOnly):
    list_display = ('estimate_row_code', 'estimate_row_long_name')


class SubSegmentAdmin(AdminreadOnly, AdminImportExport):
    list_display = ('sub_segment_code', 'sub_segment_long_name',
                    'Segment_code', 'control_budget_detail_code', 'accounting_authority_DetailCode')

    @property
    def import_info(self):
        return import_SS_class


admin.site.register(Segment, SegmentAdmin)
admin.site.register(SegmentGrandParent, SegmentGrandParentAdmin)
admin.site.register(SegmentParent, SegmentParentAdmin)
admin.site.register(SubSegment, SubSegmentAdmin)
admin.site.register(EstimateRow, EstimateRowAdmin)
