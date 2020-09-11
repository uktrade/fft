
from django import forms
from django.forms import Select

from chartofaccountDIT.models import (
    ArchivedExpenditureCategory,
    ArchivedProgrammeCode,
    ExpenditureCategory,
    ProgrammeCode,
    ProjectCode,
)


class ExpenditureTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year')
        expenditure_category = kwargs.pop('expenditure_category')

        super(ExpenditureTypeForm, self).__init__(
            *args,
            **kwargs,
        )
        if year:
            self.fields['expenditure_category_description'] = forms.ModelChoiceField(
                queryset=ArchivedExpenditureCategory.objects.filter(
                    financial_year=year
                ),
                widget=Select(),
                initial=expenditure_category,
            )
        else:
            self.fields['expenditure_category_description'] = forms.ModelChoiceField(
                queryset=ExpenditureCategory.objects.all(),
                widget=Select(),
                initial=expenditure_category,
            )

        self.fields['expenditure_category_description'].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )


class ProgrammeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year')
        programme_code = kwargs.pop('programme_code')

        super(ProgrammeForm, self).__init__(
            *args,
            **kwargs,
        )
        if year:
            self.fields['programme_code'] = forms.ModelChoiceField(
                queryset=ArchivedProgrammeCode.objects.filter(
                    financial_year=year,
                    active=True,
                ),
                widget=Select(),
                initial=programme_code,
                to_field_name="programme_code"
            )
        else:
            self.fields['programme_code'] = forms.ModelChoiceField(
                queryset=ProgrammeCode.objects.filter(
                    active=True,
                ),
                widget=Select(),
                initial=programme_code,
            )
        self.fields['programme_code'] .widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )


class ProjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        project_code = kwargs.pop('project_code')
        super(ProjectForm, self).__init__(
            *args,
            **kwargs,
        )
        self.fields['project_code'] = forms.ModelChoiceField(
            queryset=ProjectCode.objects.filter(
                active=True,
            ),
            widget=Select(),
            initial=project_code,
        )
        self.fields['project_code'].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )
