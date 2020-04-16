import datetime

from bootstrap_datepicker_plus import DatePickerInput

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import GIFT_OFFERED, GIFT_RECEIVED, GiftAndHospitality


class GiftAndHospitalityReceivedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_RECEIVED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].required = True
        # self.fields["company"].visible = False

        self.fields['classification'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['category'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['date_offered'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['grade'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['group'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company'].widget.attrs.update({'class': 'govuk-select'})

    def save(self, *args, **kwargs):
        self.instance.offer = self.offer
        self.instance.entered_date_stamp = datetime.datetime.now()
        if self.instance.group:
            self.instance.group_name = (
                self.instance.group.group_name
            )
        return super(GiftAndHospitalityReceivedForm, self).save(*args, **kwargs)

    class Meta:
        def __init__(self, *args, **kwargs):
            super(GiftAndHospitalityReceivedForm.Meta, self).__init__(*args, **kwargs)

        model = GiftAndHospitality
        fields = [
            "classification",
            "category",
            "date_offered",
            "action_taken",
            "venue",
            "reason",
            "value",
            "rep",
            "grade",
            "group",
            "company_rep",
            "company",
        ]
        labels = {
            "company": _("Company received from"),
            "company_rep": _("Company Representative received from"),
            "group": _("DIT Group offered to"),
            "rep": _("DIT Representative offered to"),
            "grade": _("DIT Representative Grade"),
        }

        widgets = {
            # 'rep' : ModelSelect2Bootstrap(url='people-autocomplete'),
            # "rep": autocomplete.ModelSelect2(url="people-autocomplete"),
            "date_offered": DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",  # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }
            ),
        }


class GiftAndHospitalityOfferedForm(GiftAndHospitalityReceivedForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_OFFERED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)

        self.fields['classification'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['category'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['date_offered'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['action_taken'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['venue'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['reason'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['value'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['grade'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['group'].widget.attrs.update({'class': 'govuk-select'})
        self.fields['company_rep'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['company'].widget.attrs.update({'class': 'govuk-select'})

    class Meta(GiftAndHospitalityReceivedForm.Meta):
        labels = {
            "company": _("Company offered to"),
            "company_rep": _("Company Representative offered to"),
            "group": _("DIT Group received from"),
            "rep": _("DIT Representative received from"),
        }
