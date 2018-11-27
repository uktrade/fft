from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import GiftAndHospitality

class GiftAndHospitalityForm(forms.ModelForm):
    class Meta:
        model = GiftAndHospitality
        fields = '__all__'
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