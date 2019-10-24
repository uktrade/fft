from core.admin import AdminActiveField, AdminImportExport

from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .import_csv import import_HR_class, import_grade_class
from .models import DITPeople, Grade


def _export_people_iterator(queryset):
    yield [
        "Name",
        "Surname",
        "Grade",
        "Cost Centre Code",
        "Cost Centre Name",
        "Directorate",
        "Group",
        "active",
    ]

    for obj in queryset:
        yield [
            obj.name,
            obj.surname,
            obj.grade.grade,
            obj.cost_centre.cost_centre_code,
            obj.cost_centre.cost_centre_name,
            obj.cost_centre.directorate.directorate_name,
            obj.cost_centre.directorate.group.group_name,
            obj.active,
        ]


class DIT_PeopleAdmin(AdminActiveField, AdminImportExport):
    list_display = ("surname", "name", "grade", "active")

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["name", "surname", "employee_number", "created", "updated"]
        else:
            return ["created", "updated"]

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ["name", "surname", "grade", "active", "created", "updated"]
        else:
            return ["name", "surname", "employee_number", "grade", "active"]

    search_fields = ["name", "surname"]
    list_filter = ("active", ("grade", RelatedDropdownFilter))

    @property
    def export_func(self):
        return _export_people_iterator

    @property
    def import_info(self):
        return import_HR_class


def _export_grade_iterator(queryset):
    yield ["Grade", "Grade Description"]

    for obj in queryset:
        yield [obj.grade, obj.gradedescription]


class GradeAdmin(AdminImportExport):
    list_display = ("grade", "gradedescription")

    @property
    def export_func(self):
        return _export_grade_iterator

    @property
    def import_info(self):
        return import_grade_class


admin.site.register(DITPeople, DIT_PeopleAdmin)
admin.site.register(Grade, GradeAdmin)
# admin.site.register(SalaryMonthlyAverage)
# admin.site.register(PayModel)
# admin.site.register(AdminPayModel)
