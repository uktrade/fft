from django.contrib import admin

from payroll.services.payroll import vacancy_created

from .models import Employee, PayElementTypeGroup, Vacancy


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "employee_no",
        "first_name",
        "last_name",
        "cost_centre",
        "has_left",
    ]
    list_filter = ["has_left"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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
        "appointee_name",
        "hiring_manager",
        "hr_ref",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            vacancy_created(obj)
