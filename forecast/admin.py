from django.contrib import admin
from django.contrib.auth import get_user_model

from simple_history.admin import SimpleHistoryAdmin

from core.admin import (
    AdminEditOnly,
    AdminImportExport,
    AdminReadOnly,
)

from forecast.forms import UnlockedForecastEditorForm
from forecast.import_csv import import_adi_file_class
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
    UnlockedForecastEditor,
)


User = get_user_model()


# def get_name(self):
#     return '{} {}'.format(self.first_name, self.last_name)
#
#
# #  TODO - swap user model to modern version, monkey patch for now
# User.add_to_class("__str__", get_name)


class MonthlyFigureAdmin(AdminImportExport, AdminReadOnly, SimpleHistoryAdmin):
    @property
    def import_info(self):
        return import_adi_file_class


class BudgetAdmin(AdminReadOnly):
    pass


class FinancialPeriodAdmin(AdminReadOnly):
    list_display = (
        "period_short_name",
        "period_long_name",
        "financial_period_code",
        "period_calendar_code",
        "actual_loaded",
        "display_figure"
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "period_long_name",
                "financial_period_code",
                "period_calendar_code",
            ]


class ForecastEditStateAdmin(AdminEditOnly, SimpleHistoryAdmin):
    history_list_display = ["locked"]


class UnlockedForecastEditorAdmin(admin.ModelAdmin):
    list_display_links = None

    form = UnlockedForecastEditorForm

    def get_form(self, request, obj=None, **kwargs):
        unlock_form = super(
            UnlockedForecastEditorAdmin,
            self,
        ).get_form(request, **kwargs)
        unlock_form.current_user = request.user
        return unlock_form


admin.site.register(ForecastMonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FinancialPeriod, FinancialPeriodAdmin)
admin.site.register(BudgetMonthlyFigure, BudgetAdmin)
admin.site.register(ForecastEditState, ForecastEditStateAdmin)
admin.site.register(UnlockedForecastEditor, UnlockedForecastEditorAdmin)
