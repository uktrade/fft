from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

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
            return ['name', 'surname', 'grade', 'isdirector', 'isbusinesspartner',
                    'active', 'created', 'updated']
        else:
            return ['name', 'surname', 'employee_number', 'grade',
                    'isdirector', 'isbusinesspartner', 'active']

    search_fields = ['name', 'surname']
    list_filter = ('active',
                   'isdirector',
                   'isbusinesspartner',
                   ('grade', RelatedDropdownFilter),
                   )


admin.site.register(Grade)
admin.site.register(DITPeople, DIT_PeopleAdmin)
admin.site.register(SalaryMonthlyAverage)
admin.site.register(PayModel)
admin.site.register(AdminPayModel)
