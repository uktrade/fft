from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from core.admin import AdminReadOnly

from end_of_month.models import EndOfMonthStatus


class EndOfMonthStatusAdmin(AdminReadOnly, SimpleHistoryAdmin):
    list_display = (
        "period_name",
        "period_code",
        "archived",
        "archived_by",
        "archived_date"
    )

    def period_name(self, instance):
        return instance.archived_period.period_long_name

    def period_code(self, instance):
        return instance.archived_period.financial_period_code


admin.site.register(EndOfMonthStatus, EndOfMonthStatusAdmin)
