from django.contrib import admin

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from core.exportutils import export_to_csv, export_to_excel

from .models import Grade, SalaryMonthlyAverage, PayModel, AdminPayModel, DITPeople


class DIT_PeopleAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'grade', 'isdirector', 'isbusinesspartner', 'active')

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'surname', 'employee_number', 'created', 'updated']
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['name', 'surname', 'grade', 'isdirector', 'isbusinesspartner', 'active', 'created', 'updated']
        else:
            return ['name', 'surname', 'employee_number', 'grade', 'isdirector', 'isbusinesspartner', 'active']

    search_fields = ['name', 'surname']
    list_filter = ('active',
                   'isdirector',
                   'isbusinesspartner',
                   ('grade', RelatedDropdownFilter),
                   )

    # actions = [export_cc_csv, export_cc_xlsx, ]


admin.site.register(Grade)
admin.site.register(DITPeople, DIT_PeopleAdmin)
admin.site.register(SalaryMonthlyAverage)
admin.site.register(PayModel)
admin.site.register(AdminPayModel)
