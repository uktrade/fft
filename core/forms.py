from django import forms
from django.forms.renderers import TemplatesSetting


class FormRenderer(TemplatesSetting):
    field_template_name = "core/forms/field.html"
    form_template_name = "core/forms/form.html"


class ModelForm(forms.ModelForm):
    error_css_class = "govuk-input--error"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            match field.widget:
                case forms.Select():
                    field.widget.attrs.update({"class": "govuk-select"})
                case forms.TextInput():
                    field.widget.attrs.update({"class": "govuk-input"})


class ChoicesWidget(forms.Select):
    template_name = "core/forms/widgets/choices.html"

    class Media:
        css = {
            "all": [
                "choices.js/public/assets/styles/choices.min.css",
            ],
        }
        js = ["choices.js/public/assets/scripts/choices.min.js"]
