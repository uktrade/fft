import io

from core.admin import AdminActiveField, AdminExport, AdminImportExport, AdminreadOnly, CsvImportForm

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .exportcsv import export_bp_iterator, export_bsce_iterator, export_cc_iterator, export_directorate_iterator, \
    export_group_iterator, export_historic_costcentre_iterator, export_person_iterator
from .importcsv import import_cc_class, import_cc_dit_specific_class, \
    import_departmental_group_class, import_director_class
from .models import BSCEEmail, BusinessPartner, CostCentre, CostCentrePerson, \
    DepartmentalGroup, Directorate, HistoricCostCentre


# Displays extra fields in the list of cost centres
class CostCentreAdmin(AdminActiveField, AdminImportExport):
    """Define an extra import button, for the DIT specific fields"""
    change_list_template = "admin/m_import_changelist.html"

    list_display = ('cost_centre_code', 'cost_centre_name', 'directorate_code',
                    'directorate_name', 'group_code', 'group_name', 'deputy_director',
                    'business_partner', 'treasury_segment', 'active')

    def directorate_name(self, instance):  # required to display the field from a foreign key
        return instance.directorate.directorate_name

    def directorate_code(self, instance):  # required to display the field from a foreign key
        return instance.directorate.directorate_code

    def group_name(self, instance):
        return instance.directorate.group.group_name

    def group_code(self, instance):
        return instance.directorate.group.group_code

    def treasury_segment(self, instance):
        return instance.directorate.group.treasury_segment_fk

    directorate_name.admin_order_field = 'directorate__directorate_name'
    directorate_code.admin_order_field = 'directorate__directorate_code'
    group_name.admin_order_field = 'directorate__group__group_name'
    group_code.admin_order_field = 'directorate__group__group_code'
    treasury_segment.admin_order_field = 'directorate__group__treasury_segment_fk'

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
                    'directorate', 'deputy_director', 'business_partner', 'bsce_email', 'used_for_travel',
                    'disabled_with_actual', 'active', 'created', 'updated']
        else:
            return ['cost_centre_code', 'cost_centre_name', 'directorate', 'bsce_email', 'used_for_travel',
                    'deputy_director', 'business_partner', 'disabled_with_actual', 'active']

    # the export and import function must be defined as properties, to stop getting 'self' as first parameter
    @property
    def export_func(self):
        return export_cc_iterator

    @property
    def import_info(self):
        return import_cc_class

    search_fields = ['cost_centre_code', 'cost_centre_name',
                     'directorate__directorate_code', 'directorate__directorate_name',
                     'directorate__group__group_code', 'directorate__group__group_name',
                     'deputy_director__name', 'deputy_director__surname']
    list_filter = ('active', 'disabled_with_actual', 'used_for_travel',
                   ('directorate', RelatedDropdownFilter),
                   ('directorate__group', RelatedDropdownFilter))

    autocomplete_fields = ['directorate']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import1-csv/', self.import1_csv),
        ]
        return my_urls + urls

    def import1_csv(self, request):
        header_list = import_cc_dit_specific_class.header_list
        import_func = import_cc_dit_specific_class.my_import_func
        form_title = import_cc_dit_specific_class.form_title
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


class DirectorateAdmin(AdminActiveField, AdminImportExport):
    list_display = ('directorate_code', 'directorate_name',
                    'group_code', 'group_name', 'director', 'active')
    search_fields = ['directorate_code', 'directorate_name',
                     'group__group_name', 'group__group_code',
                     'director__name', 'director__surname']
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
        return export_directorate_iterator

    @property
    def import_info(self):
        return import_director_class


class DepartmentalGroupAdmin(AdminActiveField, AdminImportExport):
    list_display = ('group_code', 'group_name', 'director_general', 'treasury_segment_fk', 'active')
    search_fields = ['group_code', 'group_name',
                     'director_general__name', 'director_general__surname']
    list_filter = ('active',
                   ('treasury_segment_fk', RelatedDropdownFilter))

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
            return ['group_code', 'group_name', 'director_general', 'treasury_segment_fk', 'active', 'created',
                    'updated']
        else:
            return ['group_code', 'group_name', 'director_general', 'treasury_segment_fk', 'active']

    @property
    def export_func(self):
        return export_group_iterator

    @property
    def import_info(self):
        return import_departmental_group_class


class BSCEEmailAdmin(AdminActiveField, AdminExport):
    list_display = ('bsce_email', 'active')
    search_fields = ['bsce_email']

    def get_readonly_fields(self, request, obj=None):
        return ['created', 'updated']

    @property
    def export_func(self):
        return export_bsce_iterator


class BusinessPartnerAdmin(AdminActiveField, AdminExport):
    list_display = ('bp_email', 'active')
    search_fields = ['name', 'surname', 'bp_email']

    def get_readonly_fields(self, request, obj=None):
        return ['created', 'updated']

    @property
    def export_func(self):
        return export_bp_iterator


class CostCentrePersonAdmin(AdminActiveField, AdminExport):
    list_display = ('full_name', 'is_dg', 'is_director', 'active')
    search_fields = ['name', 'surname', 'email']

    list_filter = ('active',
                   'is_director',
                   'is_dg',
                   )

    def get_readonly_fields(self, request, obj=None):
        return ['created', 'updated']

    @property
    def export_func(self):
        return export_person_iterator


class HistoricCostCentreAdmin(AdminreadOnly, AdminExport):
    list_display = ('cost_centre_code', 'cost_centre_name', 'directorate_code',
                    'directorate_name', 'group_code', 'group_name', 'deputy_director_fullname',
                    'business_partner_fullname', 'active')
    search_fields = ['cost_centre_code', 'cost_centre_name',
                     'directorate_code', 'directorate_name',
                     'group_code', 'group_name',
                     'deputy_director_fullname']
    list_filter = ('active',
                   'disabled_with_actual',
                   ('financial_year', RelatedDropdownFilter))
    fields = ('financial_year', 'cost_centre_code', 'cost_centre_name',
              'directorate_code', 'directorate_name', 'director_fullname',
              'group_code', 'group_name', 'dg_fullname',
              'deputy_director_fullname', 'business_partner_fullname', 'bsce_email',
              'disabled_with_actual', 'active', 'archived')

    @property
    def export_func(self):
        return export_historic_costcentre_iterator


admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup, DepartmentalGroupAdmin)
admin.site.register(Directorate, DirectorateAdmin)
admin.site.register(BSCEEmail, BSCEEmailAdmin)
admin.site.register(BusinessPartner, BusinessPartnerAdmin)
admin.site.register(CostCentrePerson, CostCentrePersonAdmin)
admin.site.register(HistoricCostCentre, HistoricCostCentreAdmin)
