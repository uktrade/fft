from django import forms
from django.forms import ModelForm
from forecast.models import MonthlyFigure


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
