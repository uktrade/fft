from django.contrib import admin

from .models import Grade, SalaryMonthlyAverage, VacanciesHeadCount, PayModel, PayCostHeadCount, AdminPayModel, DITPeople

admin.site.register(Grade)
admin.site.register(DITPeople)
admin.site.register(SalaryMonthlyAverage)
admin.site.register(VacanciesHeadCount)
admin.site.register(PayModel)
admin.site.register(PayCostHeadCount)
admin.site.register(AdminPayModel)
