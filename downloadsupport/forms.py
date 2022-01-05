import json

from django import forms

from core.models import FinancialYear

class DownloadMIForm(forms.Form):
    def __init__(self, *args, **kwargs):
        selected_year = kwargs.pop('selected_year', 0)
        super(DownloadMIForm, self).__init__(
            *args,
            **kwargs,
        )
        display_list = FinancialYear.financial_year_objects.future_list()
        if display_list:
            display_list.extend([(0, 'Current')])
        else:
            display_list = [(0, 'Current')]

        self.fields['selected_year'] = forms.ChoiceField(
            choices=display_list,
            initial=selected_year
        )
        self.fields["selected_year"].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )