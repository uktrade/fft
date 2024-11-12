from django import forms

from payroll.models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = "__all__"
        widgets = {
            'grade': forms.Select(attrs={'class': 'govuk-select'}),
            'programme_code': forms.Select(attrs={'class': 'govuk-select'}),
            'programme_switch_vacancy': forms.Select(attrs={'class': 'govuk-select'}),
            'appointee_name': forms.Select(attrs={'class': 'govuk-input govuk-input--width-20'}),
            'hiring_manager': forms.Select(attrs={'class': 'govuk-input govuk-input--width-20'}),
            'hr_ref': forms.Select(attrs={'class': 'govuk-input govuk-input--width-20'}),
        }
