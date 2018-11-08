from django.contrib import admin

from .models import  GiftsAndHospitalityCompany, \
    GiftsAndHospitalityCategory, GiftsAndHospitalityClassification

admin.site.register(GiftsAndHospitalityCompany)
admin.site.register(GiftsAndHospitalityCategory)
admin.site.register(GiftsAndHospitalityClassification)

