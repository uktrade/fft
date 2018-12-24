from core.tables import FadminTable

from .models import GiftAndHospitality


class GiftHospitalityTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = GiftAndHospitality
        fields = (
            'id',
            'gift_type',
            'category',
            'classification',
            'group_name',
            'date_offered',
            'venue',
            'reason',
            'value',
            'rep',
            'grade',
            'offer',
            'company_rep',
            'company',
            'action_taken',
            'entered_date_stamp',
            'entered_by',
        )
