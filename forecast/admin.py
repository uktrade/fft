from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django.contrib import admin
from django.contrib.auth import get_user_model
from simple_history.admin import SimpleHistoryAdmin

from core.admin import AdminEditOnly, AdminImportExport, AdminReadOnly
from forecast.forms import UnlockedForecastEditorForm
from forecast.import_csv import import_adi_file_class
from forecast.models import (
    BudgetMonthlyFigure,
    FinancialCode,
    FinancialPeriod,
    ForecastEditState,
    ForecastMonthlyFigure,
    FutureForecastEditState,
    UnlockedForecastEditor,
)


User = get_user_model()


class MonthlyFigureAdmin(AdminImportExport, AdminReadOnly, SimpleHistoryAdmin):
    list_display = (
        "financial_code",
        "financial_year",
        "financial_period",
        "amount",
        "archived_status",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "financial_code",
                "financial_year",
                "financial_period",
                "amount",
                "archived_status",
            ]

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
        "actual_loaded_previous_year",
        "display_figure",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "period_short_name",
                "period_long_name",
                "financial_period_code",
                "period_calendar_code",
                "actual_loaded",
                "actual_loaded_previous_year",
            ]


class ForecastEditStateAdmin(AdminEditOnly, SimpleHistoryAdmin):
    history_list_display = ["locked"]


class FutureForecastEditStateAdmin(AdminEditOnly, SimpleHistoryAdmin):
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


class FinancialCodeAdmin(AdminReadOnly):
    list_display = (
        "id",
        "cost_centre",
        "programme",
        "natural_account_code",
        "analysis1_code",
        "analysis2_code",
        "project_code",
        "forecast_expenditure_type",
    )

    search_fields = [
        "id",
        "cost_centre__cost_centre_code",
        "programme__programme_code",
        "natural_account_code__natural_account_code",
        "analysis1_code__analysis1_code",
        "analysis2_code__analysis2_code",
        "project_code__project_code",
    ]
    list_filter = (
        ("cost_centre", RelatedDropdownFilter),
        ("natural_account_code", RelatedDropdownFilter),
        ("programme", RelatedDropdownFilter),
        ("analysis1_code", RelatedDropdownFilter),
        ("analysis2_code", RelatedDropdownFilter),
        ("project_code", RelatedDropdownFilter),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                "id",
                "programme",
                "cost_centre",
                "natural_account_code",
                "analysis1_code",
                "analysis2_code",
                "project_code",
                "forecast_expenditure_type",
            ]


admin.site.register(ForecastMonthlyFigure, MonthlyFigureAdmin)
admin.site.register(FinancialPeriod, FinancialPeriodAdmin)
admin.site.register(BudgetMonthlyFigure, BudgetAdmin)
admin.site.register(ForecastEditState, ForecastEditStateAdmin)
admin.site.register(FutureForecastEditState, FutureForecastEditStateAdmin)
admin.site.register(UnlockedForecastEditor, UnlockedForecastEditorAdmin)
admin.site.register(FinancialCode, FinancialCodeAdmin)
