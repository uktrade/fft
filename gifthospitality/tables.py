from core.tables import FadminTable

import django_tables2 as tables

from .models import GiftAndHospitality


class GiftHospitalityTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = GiftAndHospitality

