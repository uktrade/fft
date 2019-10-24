from core.tables import FadminTable

from .models import GiftAndHospitality


class GiftHospitalityTable(FadminTable):
    class Meta(FadminTable.Meta):
        model = GiftAndHospitality
        fields = (
            "id",
            "category_fk",
            "classification_fk",
            "group_name",
            "date_offered",
            "venue",
            "reason",
            "value",
            "rep",
            "grade_fk",
            "offer",
            "company_rep",
            "company",
            "action_taken",
            "entered_date_stamp",
            "entered_by",
        )
