from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from core.exportutils import export_to_excel
from core.admin import AdminActiveField
from payroll.models import DITPeople
from .models import DepartmentalGroup, Directorate, CostCentre


def _export_cc_iterator(queryset):
    yield ['Cost Centre', 'Cost Centre Description', 'Active',
           'Directorate', 'Directorate Description', 'Directorate Active',
           'Group', 'Group Description', 'Group Active']
    for obj in queryset:
        yield [obj.cost_centre_code,
               obj.cost_centre_name,
               obj.active,
               obj.directorate.directorate_code,
               obj.directorate.directorate_name,
               obj.directorate.active,
               obj.directorate.group.group_code,
               obj.directorate.group.group_name,
               obj.directorate.group.active]


def export_cc_xlsx(modeladmin, request, queryset):
    return (export_to_excel(queryset, _export_cc_iterator))


export_cc_xlsx.short_description = u"Export to Excel"


# Displays extra fields in the list of cost centres
class CostCentreAdmin(AdminActiveField):
    list_display = ('cost_centre_code', 'cost_centre_name',
                    'directorate_name', 'group_name', 'active')

    def directorate_name(self, instance):  # required to display the field from a foreign key
        return instance.directorate.directorate_name

    def group_name(self, instance):
        return instance.directorate.group.group_name

    directorate_name.admin_order_field = 'directorate__directorate_name'
    group_name.admin_order_field = 'directorate__group__group_name'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "business_partner":
            kwargs["queryset"] = DITPeople.objects.filter(isbusinesspartner=True, active=True)
        if db_field.name == 'deputy_director':
            kwargs["queryset"] = DITPeople.objects.filter(isdirector=True, active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['cost_centre_code', 'created', 'updated']  # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['cost_centre_code', 'cost_centre_name',
                    'directorate', 'deputy_director', 'business_partner',
                    'active', 'created', 'updated']
        else:
            return ['cost_centre_code', 'cost_centre_name', 'directorate',
                    'deputy_director', 'business_partner', 'active']

    search_fields = ['cost_centre_code', 'cost_centre_name']
    list_filter = ('active',
                   ('directorate', RelatedDropdownFilter),
                   ('directorate__group', RelatedDropdownFilter))
    actions = [export_cc_xlsx]


def _export_directorate_iterator(queryset):
    yield ['Directorate', 'Directorate Description', 'Active',
           'Group', 'Group Description', 'Group Active']
    for obj in queryset:
        yield [obj.directorate_code,
               obj.directorate_name,
               obj.active,
               obj.group.group_code,
               obj.group.group_name,
               obj.group.active]


def export_directorate_xlsx(modeladmin, request, queryset):
    return (export_to_excel(queryset, _export_directorate_iterator))


export_directorate_xlsx.short_description = u"Export to Excel"


class DirectorateAdmin(AdminActiveField):
    list_display = ('directorate_code', 'directorate_name', 'dgroup_name', 'director', 'active')
    search_fields = ['directorate_code', 'directorate_name']
    list_filter = ('active',
                   ('group', RelatedDropdownFilter))

    def dgroup_name(self, instance):
        return instance.group.group_code + ' - ' + instance.group.group_name

    dgroup_name.admin_order_field = 'group__group_name'

    # limit the list available in the drop downs
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'director':
            kwargs["queryset"] = DITPeople.objects.filter(isdirector=True, active=True)
        if db_field.name == 'group':
            kwargs["queryset"] = DepartmentalGroup.objects.filter(active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['directorate_code', 'created', 'updated']  # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['directorate_code', 'directorate_name', 'group',
                    'director', 'active', 'created', 'updated']
        else:
            return ['directorate_code', 'directorate_name', 'group', 'director', 'active']

    actions = [export_directorate_xlsx]


def _export_group_iterator(queryset):
    yield ['Group', 'Group Description', 'Active']
    for obj in queryset:
        yield [obj.group_code,
               obj.group_name,
               obj.active]


def export_group_xlsx(modeladmin, request, queryset):
    return (export_to_excel(queryset, _export_group_iterator))


export_group_xlsx.short_description = u"Export to Excel"


class DepartmentalGroupAdmin(AdminActiveField):
    list_display = ('group_code', 'group_name', 'director_general', 'active')
    search_fields = ['group_code', 'group_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'director_general':
            kwargs["queryset"] = DITPeople.objects.filter(isdirector=True, active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['group_code', 'created', 'updated']  # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['group_code', 'group_name', 'director_general', 'active', 'created', 'updated']
        else:
            return ['group_code', 'group_name', 'director_general', 'active']

    actions = [export_group_xlsx]


admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup, DepartmentalGroupAdmin)
admin.site.register(Directorate, DirectorateAdmin)
# admin.site.register(Programme, ProgrammeAdmin)
