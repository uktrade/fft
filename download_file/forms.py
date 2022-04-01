from django import forms

from core.models import FinancialYear
from core.utils.generic_helpers import get_current_financial_year


class DownloadMIForm(forms.Form):
    def __init__(self, *args, **kwargs):
        selected_year = kwargs.pop('selected_year', 0)
        super(DownloadMIForm, self).__init__(
            *args,
            **kwargs,
        )
        current_year = get_current_financial_year()
        display_list = FinancialYear.financial_year_objects.future_list()
        if display_list:
            display_list.extend([(current_year, 'Current')])
        else:
            display_list = [(current_year, 'Current')]

        self.fields['download_year'] = forms.ChoiceField(
            choices=display_list,
            initial=selected_year
        )
        self.fields["download_year"].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )
