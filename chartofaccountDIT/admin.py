from django.contrib import admin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

from core.admin import AdminActiveField, AdminExport, AdminImportExport, AdminreadOnly
from core.exportutils import generic_table_iterator, get_fk_value

from .importcsv import import_a1_class, import_a2_class, import_NAC_expenditure_cat_class, \
    import_NAC_class, \
    import_prog_class

from .models import Analysis1, Analysis2, CommercialCategory, ExpenditureCategory, \
    NACCategory, NaturalCode, ProgrammeCode


def _export_nac_iterator(queryset):
    yield ['Level 6', 'Level 6 Description',
           'Active', 'Level 5', 'Level 5 Description',
           'Category', 'Dashboard Group']

    for obj in queryset:
        yield [obj.natural_account_code,
               obj.natural_account_code_description,
               obj.active,
               get_fk_value(obj.account_L5_code, 'account_l5_code'),
               get_fk_value(obj.account_L5_code, 'account_l5_long_name')]


class NaturalCodeAdmin(AdminreadOnly, AdminActiveField, AdminImportExport):
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


class Analysis1Admin(AdminreadOnly, AdminActiveField,  AdminImportExport):
    search_fields = ['analysis1_description', 'analysis1_code']
    list_display = ('analysis1_code', 'analysis1_description', 'active')

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_a1_class


class Analysis2Admin(AdminreadOnly,  AdminActiveField, AdminImportExport):
    search_fields = ['analysis2_description', 'analysis2_code']
    list_display = ('analysis2_code', 'analysis2_description', 'active')

    @property
    def export_func(self):
        return generic_table_iterator

    @property
    def import_info(self):
        return import_a2_class


def _export_exp_cat_iterator(queryset):
    yield ['Budget Grouping', 'Expenditure Category',
           'Description', 'Further Description', 'Budget NAC', 'Budget NAC Description'
           ]
    for obj in queryset:
        yield [obj.NAC_category.NAC_category_description,
               obj.grouping_description,
               obj.description,
               obj.further_description,
               obj.linked_budget_code.natural_account_code,
               obj.linked_budget_code.natural_account_code_description]


class ExpenditureCategoryAdmin(AdminExport):
    search_fields = ['grouping_description', 'description']
    list_display = ['grouping_description', 'description', 'NAC_category', 'linked_budget_code']
    list_filter = ('NAC_category',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "linked_budget_code":
            kwargs["queryset"] = NaturalCode.objects.filter(used_for_budget=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @property
    def export_func(self):
        return _export_exp_cat_iterator

    # @property
    # def import_func(self):
    #     return import_expenditure_category


def _export_nac_cat_iterator(queryset):
    yield ['Budget Grouping']

    for obj in queryset:
        yield [obj.NAC_category_description, ]


class NACCategoryAdmin(AdminImportExport):
    search_fields = ['NAC_category_description']
    list_display = ['NAC_category_description']

    @property
    def export_func(self):
        return _export_nac_cat_iterator

    @property
    def import_info(self):
        return import_NAC_expenditure_cat_class


def _export_programme_iterator(queryset):
    yield ['Programme Code', 'Description', 'Budget Type', 'Active']
    for obj in queryset:
        yield [obj.programme_code,
               obj.programme_description,
               obj.budget_type,
               obj.active]


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


admin.site.register(Analysis1, Analysis1Admin)
admin.site.register(Analysis2, Analysis2Admin)
admin.site.register(NaturalCode, NaturalCodeAdmin)
admin.site.register(ExpenditureCategory, ExpenditureCategoryAdmin)
admin.site.register(NACCategory, NACCategoryAdmin)
admin.site.register(CommercialCategory)
admin.site.register(ProgrammeCode, ProgrammeAdmin)
