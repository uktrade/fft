from django import forms

from payroll.models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ["cost_centre", "fte"]
        labels = {"hr_ref": "HR reference"}
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
