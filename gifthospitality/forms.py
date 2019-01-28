import datetime

from bootstrap_datepicker_plus import DatePickerInput

from dal import autocomplete

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import GIFT_OFFERED, GIFT_RECEIVED, GiftAndHospitality


class GiftAndHospitalityReceivedForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.offer = GIFT_RECEIVED
        super(GiftAndHospitalityReceivedForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].required = True
        self.fields['company'].visible = False

    def save(self, *args, **kwargs):
        self.instance.offer = self.offer
        self.instance.entered_date_stamp = datetime.datetime.now()
        if self.instance.rep_fk:
            self.instance.rep = self.instance.rep_fk
            self.instance.grade_fk = self.instance.rep_fk.grade
            self.instance.group_name = \
                self.instance.rep_fk.cost_centre.directorate.group.group_name
        return super(GiftAndHospitalityReceivedForm, self).save(*args, **kwargs)

    class Meta:
        def __init__(self, *args, **kwargs):
            super(GiftAndHospitalityReceivedForm.Meta, self).__init__(*args, **kwargs)

        model = GiftAndHospitality
        fields = [
            'classification_fk',
            'category_fk',
            'date_offered',
            'action_taken',
            'venue',
            'reason',
            'value',
            'rep_fk',
            'company_rep',
            'company_fk',
            'company'
        ]
        labels = {'company_fk': _('Company received from'),
                  'company_rep': _('Company Representative received from'),
                  'rep_fk': _('DIT Representative offered to')
                  }

        widgets = {
            # 'rep_fk' : ModelSelect2Bootstrap(url='people-autocomplete'),
            'rep_fk': autocomplete.ModelSelect2(url='people-autocomplete'),
            'date_offered': DatePickerInput(
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

    class Meta(GiftAndHospitalityReceivedForm.Meta):
        labels = {'company_fk': _('Company offered to'),
                  'company_rep': _('Company Representative offered to'),
                  'rep_fk': _('DIT Representative received from')
                  }
