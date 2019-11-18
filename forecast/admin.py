from django.contrib import admin

from core.admin import (
    AdminImportExport,
    AdminReadOnly,
)

from forecast.import_csv import import_adi_file_class
from forecast.models import (
    FinancialPeriod,
    ForecastActualBudgetFigure,
    ForecastPermission,
)


class ForecastActualBudgetFigureAdmin(AdminImportExport, AdminReadOnly):
    @property
    def import_info(self):
        return import_adi_file_class


admin.site.register(ForecastActualBudgetFigure, ForecastActualBudgetFigureAdmin)
admin.site.register(FinancialPeriod)
admin.site.register(ForecastPermission)
