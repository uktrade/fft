from django import forms

from payroll.models import Vacancy
from payroll.validators import validate_only_letters_numbers_spaces


class VacancyForm(forms.ModelForm):

    appointee_name = forms.CharField(
        validators=[
            lambda value: validate_only_letters_numbers_spaces(value, "Appointee name")
        ],
        widget=forms.TextInput(attrs={"class": "govuk-input govuk-input--width-20"}),
        required=False,
    )
    hiring_manager = forms.CharField(
        validators=[
            lambda value: validate_only_letters_numbers_spaces(value, "Hiring manager")
        ],
        widget=forms.TextInput(attrs={"class": "govuk-input govuk-input--width-20"}),
        required=False,
    )
    hr_ref = forms.CharField(
        validators=[
            lambda value: validate_only_letters_numbers_spaces(value, "HR ref")
        ],
        widget=forms.TextInput(attrs={"class": "govuk-input govuk-input--width-20"}),
        required=False,
    )

    class Meta:
        model = Vacancy
        fields = "__all__"
        exclude = ["cost_centre"]
        widgets = {
            "recruitment_type": forms.Select(attrs={"class": "govuk-select"}),
            "grade": forms.Select(attrs={"class": "govuk-select"}),
            "recruitment_stage": forms.Select(attrs={"class": "govuk-select"}),
            "programme_code": forms.Select(attrs={"class": "govuk-select"}),
        }
        error_messages = {
            "grade": {
                "required": "Grade is a required field.",
            },
            "programme_code": {
                "required": "Programme code is a required field.",
            },
        }
