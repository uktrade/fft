from django import forms
from .models import GiftAndHospitality

class GiftAndHospitalityForm(forms.ModelForm):
    class Meta:
        model = GiftAndHospitality
        fields = '__all__'
