
from django import forms
from django.forms import Select

from chartofaccountDIT.models import ExpenditureCategory, ProgrammeCode


class ExpenditureTypeForm(forms.Form):
    expenditure_category = forms.ModelChoiceField(
        queryset=ExpenditureCategory.objects.all(),
        widget=Select(),
    )
    expenditure_category.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )


class ProgrammeForm(forms.Form):
    programme_code = forms.ModelChoiceField(
        queryset=ProgrammeCode.objects.filter(
            active=True,
        ),
        widget=Select(),
    )
    programme_code.widget.attrs.update(
        {
            "class": "govuk-select",
        }
    )
