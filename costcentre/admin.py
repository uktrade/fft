import io

from core.admin import AdminActiveField, AdminExport, AdminImportExport, CsvImportForm

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path


from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .importcsv import import_cc_class, import_cc_people_class, \
    import_departmental_group_class, import_director_class
from .models import BSCEEmail, BusinessPartner, CostCentre, CostCentrePerson, \
    DepartmentalGroup, Directorate


def _export_cc_iterator(queryset):
    yield ['Cost Centre', 'Cost Centre Description', 'Active',
           'Directorate', 'Directorate Description', 'Directorate Active',
           'Group', 'Group Description', 'Group Active',
           'BSCE Email']
    for obj in queryset:
        yield [obj.cost_centre_code,
               obj.cost_centre_name,
               obj.active,
               obj.directorate.directorate_code,
               obj.directorate.directorate_name,
               obj.directorate.active,
               obj.directorate.group.group_code,
               obj.directorate.group.group_name,
               obj.directorate.group.active,
               obj.bsce_email]


# Displays extra fields in the list of cost centres
class CostCentreAdmin(AdminActiveField, AdminImportExport):
    """Define an extra import button, for the DIT specific fields"""
    change_list_template = "admin/m_import_changelist.html"

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
            kwargs["queryset"] = BusinessPartner.objects.filter(active=True)
        if db_field.name == 'deputy_director':
            kwargs["queryset"] = CostCentrePerson.objects.filter(active=True)
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
                    'directorate', 'deputy_director', 'business_partner', 'bsce_email',
                    'active', 'created', 'updated']
        else:
            return ['cost_centre_code', 'cost_centre_name', 'directorate','bsce_email',
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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import1-csv/', self.import1_csv),
        ]
        return my_urls + urls

    def import1_csv(self, request):
        header_list = import_cc_people_class.header_list
        import_func = import_cc_people_class.my_import_func
        form_title = import_cc_people_class.form_title
        if request.method == "POST":
            form = CsvImportForm(header_list, form_title, request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]
                # read() gives you the file contents as a bytes object,
                # on which you can call decode().
                # decode('cp1252') turns your bytes into a string, with known encoding.
                # cp1252 is used to handle single quotes in the strings
                t = io.StringIO(csv_file.read().decode('cp1252'))
                import_func(t)
                return redirect("..")
        else:
            form = CsvImportForm(header_list, form_title)
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


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


class DirectorateAdmin(AdminActiveField, AdminImportExport):
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
            kwargs["queryset"] = CostCentrePerson.objects.filter(is_director=True, active=True)
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

    @property
    def import_info(self):
        return import_director_class


def _export_group_iterator(queryset):
    yield ['Group', 'Group Description', 'Active']
    for obj in queryset:
        yield [obj.group_code,
               obj.group_name,
               obj.active]


class DepartmentalGroupAdmin(AdminActiveField, AdminImportExport):
    list_display = ('group_code', 'group_name', 'director_general', 'active')
    search_fields = ['group_code', 'group_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'director_general':
            kwargs["queryset"] = CostCentrePerson.objects.filter(is_dg=True, active=True)
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

    @property
    def import_info(self):
        return import_departmental_group_class



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
        return _export_bsce_iterator


def _export_bp_iterator(queryset):
    yield ['BSCE Email', 'Active']
    for obj in queryset:
        yield [obj.bsce_email,
               obj.active]


class BusinessPartnerAdmin(AdminActiveField, AdminExport):
    list_display = ('bp_email', 'active')
    search_fields = ['name', 'surname', 'bp_email']

    def get_readonly_fields(self, request, obj=None):
        return [ 'created', 'updated']

    @property
    def export_func(self):
        return _export_bp_iterator


def _export_person_iterator(queryset):
    yield ['BSCE Email', 'Active']
    for obj in queryset:
        yield [obj.bsce_email,
               obj.active]


class CostCentrePersonAdmin(AdminActiveField, AdminExport):
    list_display = ('surname', 'name','is_dg', 'is_director', 'active')
    search_fields = ['name', 'surname', 'email']

    list_filter = ('active',
                   'is_director',
                   'is_dg',
                   )

    def get_readonly_fields(self, request, obj=None):
        return [ 'created', 'updated']

    @property
    def export_func(self):
        return _export_bp_iterator


admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup, DepartmentalGroupAdmin)
admin.site.register(Directorate, DirectorateAdmin)
admin.site.register(BSCEEmail, BSCEEmailAdmin)
admin.site.register(BusinessPartner, BusinessPartnerAdmin)
admin.site.register(CostCentrePerson, CostCentrePersonAdmin)
