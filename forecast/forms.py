
from django import forms


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
