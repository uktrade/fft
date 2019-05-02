from core.archive import archive_generic

from .models import HistoricL5Account, L5Account


def archive_treasury_l5(year):
    return archive_generic(year, HistoricL5Account, L5Account)
