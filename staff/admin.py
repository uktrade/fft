from django.contrib import admin

from staff.services.staff import staff_created

from .models import Staff, StaffForecast, Payroll, PayElement, PayElementGroup


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "employee_no",
        "first_name",
        "last_name",
        "cost_centre",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            staff_created(obj)


@admin.register(StaffForecast)
class StaffForecastAdmin(admin.ModelAdmin):
    list_display = [
        "staff",
        "year",
        "period_1",
        "period_2",
        "period_3",
        "period_4",
        "period_5",
        "period_6",
        "period_7",
        "period_8",
        "period_9",
        "period_10",
        "period_11",
        "period_12",
    ]


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = [
        "staff",
        "pay_element",
        "debit_amount",
        "credit_amount",
    ]


@admin.register(PayElement)
class PayElementAdmin(admin.ModelAdmin):
    pass


@admin.register(PayElementGroup)
class PayElementGroupAdmin(admin.ModelAdmin):
    pass
