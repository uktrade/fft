from core.archive import archive_generic

from .models import HistoricL5Account, L5Account

def archive_treasury_l5(year):
    archive_generic(HistoricL5Account, L5Account)