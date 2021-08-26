from core.archive import archive_generic

from treasurySS.models import ArchivedSubSegment, SubSegment


def archive_treasury_segment(year):
    return archive_generic(year, ArchivedSubSegment, SubSegment)
