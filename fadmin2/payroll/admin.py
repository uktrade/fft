from django.contrib import admin

from .models import Grade, SalaryMonthlyAverage, VacanciesHeadCount, PayModel, PayCostHeadCount, AdminPayModel

admin.site.register(Grade)
admin.site.register(SalaryMonthlyAverage)
admin.site.register(VacanciesHeadCount)
admin.site.register(PayModel)
admin.site.register(PayCostHeadCount)
admin.site.register(AdminPayModel)
