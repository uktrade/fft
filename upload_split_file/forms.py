from django import forms


class UploadPercentageForm(forms.Form):
    file = forms.FileField()
    file.widget.attrs.update(
        {"class": "govuk-select", "aria-describedby": "file-hint file-error", }
    )
