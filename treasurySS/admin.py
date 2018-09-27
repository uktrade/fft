from django.contrib import admin

from .models import EstimateRow, Segment, SegmentGrandParent, SegmentParent, SubSegment

admin.site.register(Segment)
admin.site.register(SegmentGrandParent)
admin.site.register(SegmentParent)
admin.site.register(SubSegment)
admin.site.register(EstimateRow)
