from django import forms
from django.forms import ModelForm
from forecast.models import MonthlyFigure


class AddForecastRowFormCommitException(Exception):
    pass


class EditForm(forms.Form):
    cell_data = forms.CharField(widget=forms.Textarea)
    cost_centre_code = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=123
    )
    financial_year = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=123
    )


class AddForecastRowForm(ModelForm):
    class Meta:
        model = MonthlyFigure
        fields = [
            'programme',
            'natural_account_code',
            'analysis1_code',
            'analysis2_code',
            'project_code',
        ]

    def save(self, commit=True, *args, **kwargs):
        forecast_row = super(AddForecastRowForm, self).save(
            commit=False,
            *args,
            **kwargs
        )
        if commit:
            raise AddForecastRowFormCommitException(
                "This form should not be used to save instances, use with commit=False"
            )
        return forecast_row
