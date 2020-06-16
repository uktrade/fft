import datetime
from datetime import date

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import GIFT_OFFERED, GIFT_RECEIVED, GiftAndHospitality


class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(
                attrs={
                    'class': 'govuk-date-input__item govuk-input govuk-input--width-2',
                    'placeholder': 'DD'}),
            forms.NumberInput(
                attrs={
                    'class': 'govuk-date-input__item govuk-input govuk-input--width-2',
                    'placeholder': 'MM'}),
            forms.NumberInput(
                attrs={
                    'class': 'govuk-date-input__item govuk-input govuk-input--width-3',
                    'placeholder': 'YYYY'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        return '{}-{}-{}'.format(year, month, day)


class GiftAndHospitalityReceivedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_RECEIVED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].required = True
        self.fields['classification'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['category'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['grade'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['group'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company'].widget.attrs.update({'class': 'govuk-select',
                                                    'onChange': 'checkOther()'})
        self.fields['company_name'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company_name'].required = False

    def save(self, *args, **kwargs):
        self.instance.offer = self.offer
        self.instance.entered_date_stamp = datetime.datetime.now()
        if self.instance.group:
            self.instance.group_name = (
                self.instance.group.group_name
            )
        return super(GiftAndHospitalityReceivedForm, self).save(*args, **kwargs)

    class Meta(DateSelectorWidget):
        def __init__(self, *args, **kwargs):
            super(GiftAndHospitalityReceivedForm.Meta, self).__init__(*args, **kwargs)

        model = GiftAndHospitality
        fields = [
            "classification",
            "category",
            "date_agreed",
            "action_taken",
            "venue",
            "reason",
            "value",
            "rep",
            "grade",
            "group",
            "company_rep",
            "company",
            "company_name",
        ]
        labels = {
            "company": _("Company received from"),
            "company_name": _("Please enter other company"),
            "company_rep": _("Company Representative received from"),
            "group": _("DIT Group offered to"),
            "rep": _("DIT Representative offered to"),
            "grade": _("DIT Representative Grade"),
        }

        widgets = {
            "date_agreed": DateSelectorWidget(

            ),
        }

        help_texts = {
            "date_agreed": _("Please use the following format: <em>YYYY-MM-DD</em>."),
        }


class GiftAndHospitalityOfferedForm(GiftAndHospitalityReceivedForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_OFFERED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)

        self.fields['classification'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['category'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['grade'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['group'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company'].widget.attrs.update({'class': 'govuk-select',
                                                    'onChange': 'checkOther()'})
        self.fields['company_name'].widget.attrs.update({'class': 'govuk-input'})

    class Meta(GiftAndHospitalityReceivedForm.Meta):
        labels = {
            "company": _("Company offered to"),
            "company_name": _("Please enter other company"),
            "company_rep": _("Company Representative offered to"),
            "group": _("DIT Group received from"),
            "rep": _("DIT Representative received from"),
            "date_agreed": _("Date of event / gift offered"),
        }
