from django import forms

from payroll.models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = "__all__"
        exclude = ["cost_centre", "fte"]
        widgets = {
            "recruitment_type": forms.Select(attrs={"class": "govuk-select"}),
            "grade": forms.Select(attrs={"class": "govuk-select"}),
            "recruitment_stage": forms.Select(attrs={"class": "govuk-select"}),
            "programme_code": forms.Select(attrs={"class": "govuk-select"}),
            "appointee_name": forms.TextInput(
                attrs={"class": "govuk-input govuk-input--width-20"}
            ),
            "hiring_manager": forms.TextInput(
                attrs={"class": "govuk-input govuk-input--width-20"}
            ),
            "hr_ref": forms.TextInput(
                attrs={"class": "govuk-input govuk-input--width-20"}
            ),
        }
