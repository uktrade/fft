import json

from django import forms

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
        data = self.cleaned_data["pasted_at_row"]

        if not data:
            return None

        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError("invalid row data supplied")

        return json_data