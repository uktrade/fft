from core.admin import AdminAsyncImportExport, AdminImportExport, AdminreadOnly

from django.contrib import admin

from .import_csv import import_adi_file_class
from .models import FinancialPeriod, MonthlyFigure


class MonthlyFigureAdmin(AdminImportExport, AdminreadOnly):

    @property
    def import_info(self):
        return import_adi_file_class


admin.site.register(MonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FinancialPeriod)
