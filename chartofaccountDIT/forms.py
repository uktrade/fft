
from django import forms
from django.forms import Select

from chartofaccountDIT.models import (
    ExpenditureCategory,
    ProgrammeCode,
    ProjectCode,
)


class ExpenditureTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        expenditure_category = kwargs.pop('expenditure_category')

        super(ExpenditureTypeForm, self).__init__(
            *args,
            **kwargs,
        )
        self.fields['expenditure_category'] = forms.ModelChoiceField(
            queryset=ExpenditureCategory.objects.all(),
            widget=Select(),
            initial=expenditure_category,
        )
        self.fields['expenditure_category'].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )


class ProgrammeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        programme_code = kwargs.pop('programme_code')

        super(ProgrammeForm, self).__init__(
            *args,
            **kwargs,
        )
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
