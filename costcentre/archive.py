from core.archive import archive_generic

from .models import CostCentre, HistoricCostCentre


def archive_cost_centre(year):
    archive_generic(year, HistoricCostCentre, CostCentre )

