from django import forms
from django.forms import Select

from chartofaccountDIT.models import ExpenditureCategory

from costcentre.models import CostCentre

from forecast.permission_shortcuts import get_objects_for_user


class CostCentreViewModeForm(forms.Form):
    COST_CENTRE_MODES = [
        ('all', 'All cost centres'),
        ('my', 'My cost centres'),
    ]

    mode = forms.ChoiceField(
        choices=COST_CENTRE_MODES,
        widget=forms.RadioSelect,
    )

    mode.widget.attrs.update(
        {
            'onclick': 'swapCostCentreChoice(this)',
        }
    )


class AllCostCentresForm(forms.Form):
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


class DirectorateCostCentresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        directorate_code = kwargs.pop('directorate_code')

        super(DirectorateCostCentresForm, self).__init__(
            *args,
            **kwargs,
        )

        self.fields['cost_centre'] = forms.ModelChoiceField(
            queryset=CostCentre.objects.filter(
                directorate__directorate_code=directorate_code,
                active=True,
            ),
            widget=Select(),
        )

        self.fields["cost_centre"].widget.attrs.update(
            {
                "class": "govuk-select",
                "aria-describedby": "cost_centre-hint cost_centre-error",
            }
        )


class MyCostCentresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MyCostCentresForm, self).__init__(
            *args,
            **kwargs,
        )
        self.base_fields['cost_centre'].queryset = get_objects_for_user(
            user,
            "costcentre.change_costcentre",
        )

    cost_centre = forms.ModelChoiceField(
        queryset=None,
        widget=Select(),
    )

    cost_centre.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "cost_centre-hint cost_centre-error",
        }
    )


class ExpenditureTypeForm(forms.Form):
    expenditure_category = forms.ModelChoiceField(
        queryset=ExpenditureCategory.objects.all(),
        widget=Select(),
    )
    # TO ASK cost_centre-hint cost_centre-error
    expenditure_category.widget.attrs.update(
        {
            "class": "govuk-select",
            "aria-describedby": "cost_centre-hint cost_centre-error",
        }
    )
