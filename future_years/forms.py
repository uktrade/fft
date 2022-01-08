from django import forms

from core.models import FinancialYear


class DownloadFutureForm(forms.Form):

    def __init__(self, *args, **kwargs):
        selected_year = kwargs.pop('selected_year', 0)
        super(DownloadFutureForm, self).__init__(
            *args,
            **kwargs,
        )
        display_list = FinancialYear.financial_year_objects.future_list()

        self.fields['download_year'] = forms.ChoiceField(
            choices=display_list,
            initial=selected_year
        )
        self.fields["download_year"].widget.attrs.update(
            {
                "class": "govuk-select",
            }
        )
