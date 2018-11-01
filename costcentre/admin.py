from core.admin import AdminActiveField, AdminExport, AdminImportExport

from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from payroll.models import DITPeople

from .importcsv import import_cc_class
from .models import BSCEEmail, CostCentre, DepartmentalGroup, Directorate


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


# Displays extra fields in the list of cost centres
class CostCentreAdmin(AdminActiveField, AdminImportExport):
    list_display = ('cost_centre_code', 'cost_centre_name', 'directorate_code',
                    'directorate_name', 'group_code', 'group_name', 'active')

    def directorate_name(self, instance):  # required to display the field from a foreign key
        return instance.directorate.directorate_name

    def directorate_code(self, instance):  # required to display the field from a foreign key
        return instance.directorate.directorate_code

    def group_name(self, instance):
        return instance.directorate.group.group_name

    def group_code(self, instance):
        return instance.directorate.group.group_code

    directorate_name.admin_order_field = 'directorate__directorate_name'
    directorate_code.admin_order_field = 'directorate__directorate_code'
    group_name.admin_order_field = 'directorate__group__group_name'
    group_code.admin_order_field = 'directorate__group__group_code'

    # limit the entries for specific foreign fields
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

    # the export and import function must be defined as properties, to stop getting 'self' as first
    # parameter
    @property
    def export_func(self):
        return _export_cc_iterator

    @property
    def import_info(self):
        return import_cc_class

    search_fields = ['cost_centre_code', 'cost_centre_name']
    list_filter = ('active',
                   ('directorate', RelatedDropdownFilter),
                   ('directorate__group', RelatedDropdownFilter))


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


class DirectorateAdmin(AdminActiveField, AdminExport):
    list_display = ('directorate_code', 'directorate_name',
                    'group_code', 'group_name', 'director', 'active')
    search_fields = ['directorate_code', 'directorate_name']
    list_filter = ('active',
                   ('group', RelatedDropdownFilter))

    def group_name(self, instance):
        return instance.group.group_name

    def group_code(self, instance):
        return instance.group.group_code

    group_name.admin_order_field = 'group__group_name'
    group_code.admin_order_field = 'group__group_code'

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

    @property
    def export_func(self):
        return _export_directorate_iterator


def _export_group_iterator(queryset):
    yield ['Group', 'Group Description', 'Active']
    for obj in queryset:
        yield [obj.group_code,
               obj.group_name,
               obj.active]


class DepartmentalGroupAdmin(AdminActiveField, AdminExport):
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

    @property
    def export_func(self):
        return _export_group_iterator


def _export_bsce_iterator(queryset):
    yield ['BSCE Email', 'Active']
    for obj in queryset:
        yield [obj.bsce_email,
               obj.active]



class BSCEEmailAdmin(AdminActiveField, AdminExport):
    list_display = ('bsce_email', 'active')
    search_fields = ['bsce_email']

    def get_readonly_fields(self, request, obj=None):
        return [ 'created', 'updated']

    @property
    def export_func(self):
        return _export_group_iterator


admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup, DepartmentalGroupAdmin)
admin.site.register(Directorate, DirectorateAdmin)
admin.site.register(BSCEEmail, BSCEEmailAdmin)
