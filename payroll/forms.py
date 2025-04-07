from core.forms import ChoicesWidget, ModelForm
from payroll.models import Vacancy


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            "recruitment_type",
            "grade",
            "recruitment_stage",
            "programme_code",
            "appointee_name",
            "hiring_manager",
            "hr_ref",
        ]
        widgets = {
            "programme_code": ChoicesWidget,
        }
