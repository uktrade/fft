import json
import logging

from django import forms

logger = logging.getLogger(__name__)

# Form for pasting HR data into the payroll table
class PasteHRForm(forms.Form):
    """
         A form for handling pasted data in an HR system.

         Attributes:
             all_selected: A hidden boolean field that indicates whether all rows are selected.
             pasted_at_row: A hidden char field that indicates the row where the data is pasted.
             paste_content: A hidden char field that holds the pasted content.

         Methods:
             clean_pasted_at_row: Cleans and validates the pasted_at_row field's data.
    """
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