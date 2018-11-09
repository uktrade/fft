import io

from core.admin import AdminActiveField, AdminExport, \
    AdminImportExport, AdminreadOnly, CsvImportForm
from core.exportutils import generic_table_iterator

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from .importcsv import import_NAC_DIT_class, import_NAC_category_class, import_NAC_class, \
    import_a1_class, import_a2_class, \
    import_comm_cat_class, import_expenditure_category_class, import_inter_entity_class,\
    import_prog_class
from .models import Analysis1, Analysis2, CommercialCategory, ExpenditureCategory, \
    InterEntityL1, InterEntity, NACCategory, NaturalCode, ProgrammeCode, ProjectCode
from .exportcsv import _export_comm_cat_iterator, _export_exp_cat_iterator, \
    _export_inter_entity_l1_iterator, _export_nac_cat_iterator, _export_nac_iterator, \
    _export_programme_iterator



class NaturalCodeAdmin(AdminreadOnly, AdminActiveField, AdminImportExport):
    """Define an extra import button, for the DIT specific fields"""
    change_list_template = "admin/m_import_changelist.html"

    list_display = ('natural_account_code', 'natural_account_code_description', 'active')

    def get_readonly_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description', 'account_L5_code']

    def get_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description',
                'account_L5_code', 'expenditure_category',
                'commercial_category', 'used_for_budget', 'active']

    search_fields = ['natural_account_code', 'natural_account_code_description']
    list_filter = ('active',
                   'used_for_budget',
                   ('expenditure_category__NAC_category', RelatedDropdownFilter),
                   ('expenditure_category', RelatedDropdownFilter))

    @property
    def export_func(self):
        return _export_nac_iterator

    @property
    def import_info(self):
        return import_NAC_class

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import1-csv/', self.import1_csv),
        ]
        return my_urls + urls

    def import1_csv(self, request):
        header_list = import_NAC_DIT_class.header_list
        import_func = import_NAC_DIT_class.my_import_func
        form_title = import_NAC_DIT_class.form_title
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


class Analysis1Admin(AdminActiveField, AdminImportExport):
    search_fields = ['analysis1_description', 'analysis1_code']
    list_display = ('analysis1_code', 'analysis1_description', 'active')

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['analysis1_code', 'created', 'updated']  # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['analysis1_code', 'analysis1_description',
                    'supplier', 'pc_reference',
                    'active', 'created', 'updated']
        else:
            return ['analysis1_code', 'analysis1_description',
                    'supplier', 'pc_reference', 'active']

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_a1_class


class Analysis2Admin(AdminActiveField, AdminImportExport):
    search_fields = ['analysis2_description', 'analysis2_code']
    list_display = ('analysis2_code', 'analysis2_description', 'active')

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['analysis2_code', 'created', 'updated']  # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['analysis2_code', 'analysis2_description',
                    'active', 'created', 'updated']
        else:
            return ['analysis2_code', 'analysis2_description','active']

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_a2_class


class ExpenditureCategoryAdmin(AdminImportExport):
    search_fields = ['grouping_description', 'description']
    list_display = ['grouping_description', 'description', 'NAC_category', 'linked_budget_code']
    list_filter = ('NAC_category',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "linked_budget_code":
            kwargs["queryset"] = NaturalCode.objects.filter(used_for_budget=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        return ['created', 'updated']

    def get_fields(self, request, obj=None):
        if obj:
            return ['grouping_description', 'description',
                    'further_description', 'linked_budget_code',
                    'NAC_category',
                    'created', 'updated']
        else:
            return ['grouping_description', 'description',
                    'further_description', 'linked_budget_code',
                    'NAC_category']

    @property
    def export_func(self):
        return _export_exp_cat_iterator

    @property
    def import_info(self):
        return import_expenditure_category_class


class CommercialCategoryAdmin(AdminImportExport):
    search_fields = ['commercial_category', 'description']
    list_display = ['commercial_category', 'description', 'commercial_category']

    @property
    def export_func(self):
        return _export_comm_cat_iterator

    @property
    def import_info(self):
        return import_comm_cat_class


class NACCategoryAdmin(AdminImportExport):
    search_fields = ['NAC_category_description']
    list_display = ['NAC_category_description']

    @property
    def export_func(self):
        return _export_nac_cat_iterator

    @property
    def import_info(self):
        return import_NAC_category_class


class ProgrammeAdmin(AdminActiveField, AdminImportExport):
    list_display = ('programme_code', 'programme_description', 'budget_type', 'active')
    search_fields = ['programme_code', 'programme_description']
    list_filter = ['budget_type', 'active']

    def get_readonly_fields(self, request, obj=None):
        return ['programme_code', 'programme_description', 'budget_type', 'created',
                'updated']  # don't allow to edit the code

    def get_fields(self, request, obj=None):
        return ['programme_code', 'programme_description',
                'budget_type', 'active', 'created', 'updated']

    @property
    def export_func(self):
        return _export_programme_iterator

    @property
    def import_info(self):
        return import_prog_class


class InterEntityL1Admin(AdminActiveField, AdminExport):
    search_fields = ['l1_value', 'l1_description']
    @property
    def export_func(self):
        return _export_inter_entity_l1_iterator


def _export_inter_entity_iterator(queryset):
    yield ['L1 Value', 'L1 Description', 'L2 Value', 'L2 Description',
           'CPID', 'Active'
           ]
    for obj in queryset:
        yield [obj.l1_value.l1_value,
               obj.l1_value.l1_description,
               obj.l2_value,
               obj.l2_description,
               obj.cpid,
               obj.active]


class InterEntityAdmin(AdminActiveField, AdminImportExport):
    list_display = ('l2_value', 'l2_description', 'l1_value', 'active')
    search_fields = ['l2_value', 'l2_description']
    list_filter = ('active', 'l1_value'
                   )

    @property
    def export_func(self):
        return _export_inter_entity_iterator

    @property
    def import_info(self):
        return import_inter_entity_class


class ProjectCodeAdmin(AdminActiveField, AdminImportExport):
    search_fields = ['project_description', 'project_code']
    list_display = ('project_code', 'project_description', 'active')

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['project_code', 'created', 'updated']  # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['project_code', 'project_description',
                    'active', 'created', 'updated']
        else:
            return ['project_code', 'project_description','active']

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_a2_class



admin.site.register(Analysis1, Analysis1Admin)
admin.site.register(Analysis2, Analysis2Admin)
admin.site.register(NaturalCode, NaturalCodeAdmin)
admin.site.register(ExpenditureCategory, ExpenditureCategoryAdmin)
admin.site.register(NACCategory, NACCategoryAdmin)
admin.site.register(CommercialCategory, CommercialCategoryAdmin)
admin.site.register(ProgrammeCode, ProgrammeAdmin)
admin.site.register(InterEntityL1, InterEntityL1Admin)
admin.site.register(InterEntity, InterEntityAdmin)
admin.site.register(ProjectCode, ProjectCodeAdmin)
