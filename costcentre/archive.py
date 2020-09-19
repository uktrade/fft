from core.archive import archive_generic

from .models import (
    ArchivedCostCentre,
    CostCentre,
)


def archive_cost_centre(year):
    return archive_generic(year, ArchivedCostCentre, CostCentre)
