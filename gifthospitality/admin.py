from django.contrib import admin

from .models import  GiftAndHospitalityCompany, \
    GiftAndHospitalityCategory, GiftAndHospitalityClassification


admin.site.register(GiftAndHospitalityCompany)
admin.site.register(GiftAndHospitalityCategory)
admin.site.register(GiftAndHospitalityClassification)

