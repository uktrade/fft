from core.tables import FadminTable

import django_tables2 as tables

from .models import GiftAndHospitality


class GiftHospitalityTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = GiftAndHospitality
        fields = (
            # 'classification_fk',
            'classification',
            'group_name',
            'date_offered',
            'venue',
            'reason',
            'value',
            'band',
            'rep',
            'offer',
            'company_rep',
            # 'company_fk',
            'company',
            'action_taken',
            'entered_by',
            'staff_no',
            'entered_date_stamp',
            # 'category_fk',
            'category',
            'grade'

        )

