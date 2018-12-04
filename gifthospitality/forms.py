from django import forms
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
from .models import GiftAndHospitality

class GiftAndHospitalityForm(forms.ModelForm):
    class Meta:
        model = GiftAndHospitality
        fields = [
            'classification_fk',
            'category_fk',
            'date_offered',
            'offer',
            'action_taken',
            'venue',
            'reason',
            'value',
            'rep_fk',
            'company_rep',
            'company_fk'
        ]
        # labels = {'classification_fk': _('AAAA')}
        # fields =['classification','group_name', 'date_offered', 'venue', 'reason']
        widgets = {
            'date_offered': DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",  # moment date-time format
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }
            ), # default date-format %m/%d/%Y will be used
            # 'end_date': DatePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
