from django import forms
from django.forms import Select

from costcentre.models import CostCentre


class ChooseCostCentreForm(forms.Form):
    cost_centre = forms.ModelChoiceField(
        queryset=CostCentre.objects.filter(
            active=True,
        ),
        widget=Select(),
    )

    cost_centre.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "cost_centre-hint cost_centre-error",
        }
    )
