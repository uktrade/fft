import json
import logging

from django import forms

logger = logging.getLogger(__name__)

# Form for pasting HR data into the payroll table
class PasteHRForm(forms.Form):
    all_selected = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    pasted_at_row = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    paste_content = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    def clean_pasted_at_row(self):
        data = dict(self.data.lists())

        if not data:
            return None

        try:
            return data
        except json.JSONDecodeError:
            raise forms.ValidationError("invalid row data supplied")