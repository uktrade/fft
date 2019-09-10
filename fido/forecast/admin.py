from core.admin import AdminAsyncImportExport, AdminreadOnly

from django.contrib import admin

from .importcsv import import_adi_file_class
from .models import FinancialPeriod, MonthlyFigure


class MonthlyFigureAdmin(AdminAsyncImportExport, AdminreadOnly):

    @property
    def import_info(self):
        return import_adi_file_class


admin.site.register(MonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FinancialPeriod)
