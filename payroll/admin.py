from django.contrib import admin

from payroll.services.payroll import employee_created

from .models import (
    Employee,
    EmployeePayElement,
    EmployeePayPeriods,
    PayElementType,
    PayElementTypeGroup,
    Vacancy,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "employee_no",
        "first_name",
        "last_name",
        "cost_centre",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            employee_created(obj)


@admin.register(EmployeePayPeriods)
class EmployeePayPeriodsAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
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
    list_filter = [
        "year",
    ]


@admin.register(EmployeePayElement)
class EmployeePayElementAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "type",
        "debit_amount",
        "credit_amount",
    ]


@admin.register(PayElementType)
class PayElementTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "natural_code",
        "group",
    ]


@admin.register(PayElementTypeGroup)
class PayElementTypeGroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "natural_code",
    ]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        "cost_centre",
        "grade",
        "programme_code",
        "programme_switch_vacancy",
        "appointee_name",
        "hiring_manager",
        "hr_ref",
    ]
