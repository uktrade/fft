from django import forms
from django.forms.widgets import (
    Textarea,
    Select,
    CheckboxInput,
    TextInput,
    EmailInput
)


class GovFormattedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if isinstance(widget, Textarea):
                widget.attrs.update({'class': 'govuk-textarea'})
            elif isinstance(widget, Select):
                widget.attrs.update({'class': 'govuk-select'})
            elif isinstance(widget, CheckboxInput):
                widget.attrs.update({'class': 'govuk-checkboxes__input'})
            elif isinstance(widget, TextInput) or isinstance(widget, EmailInput):
                widget.attrs.update({'class': 'govuk-input'})
