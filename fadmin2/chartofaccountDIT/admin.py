from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter


from core.exportutils import export_to_csv, export_to_excel, generic_export_to_csv, generic_export_to_excel
from core.admin import AdminreadOnly, AdminActiveField, AdminEditOnly

from .models import Analysis1, Analysis2, NaturalCode, ExpenditureCategory, NACCategory, CommercialCategory, ProgrammeCode


def _export_nac_iterator(queryset):
    yield ['Level 6', 'Level 6 Description',
           'Active', 'Level 5', 'Level 5 Description',
           'Category','Dashboard Group']

    for obj in queryset:
        yield[obj.natural_account_code,
            obj.natural_account_code_description,
            obj.active,
            obj.account_L5_code.account_l5_code,
            obj.account_L5_code.account_l5_long_name]


def export_nac_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_nac_iterator))


def export_nac_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_nac_iterator))


export_nac_xlsx.short_description = u"Export to Excel"
export_nac_csv.short_description = u"Export to csv"

    
class NaturalCodeAdmin(AdminreadOnly):

    list_display = ('natural_account_code', 'natural_account_code_description', 'active')

    def get_readonly_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description', 'account_L5_code']

    def get_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description', 'account_L5_code', 'expenditure_category',
                'commercial_category','used_for_budget','active']

    search_fields = ['natural_account_code','natural_account_code_description']
    list_filter = ('active',
                   'used_for_budget',
                   ('expenditure_category__NAC_category', RelatedDropdownFilter),
                   ('expenditure_category', RelatedDropdownFilter))
    actions = [export_nac_xlsx]


def export_analysis1_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_analysis1_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class Analysis1Admin(AdminreadOnly):
    search_fields = ['analysis1_description','analysis1_code']
    actions = [export_analysis1_xlsx] # new action to export to csv and xlsx


def export_analysis2_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_analysis2_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class Analysis2Admin(AdminreadOnly):
    search_fields = ['analysis2_description','analysis2_code']

    actions = [export_analysis2_xlsx] # new action to export to csv and xlsx



def export_ExpenditureCategory_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_ExpenditureCategory_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class ExpenditureCategoryAdmin(admin.ModelAdmin):
    search_fields = ['grouping_description', 'linked_budget_code']
    list_display = ['grouping_description', 'linked_budget_code']
    actions = [export_ExpenditureCategory_csv, export_ExpenditureCategory_xlsx]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "linked_budget_code":
            kwargs["queryset"] = NaturalCode.objects.filter(used_for_budget=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


def export_NACCategory_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_NACCategory_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class NACCategoryAdmin(admin.ModelAdmin):
     actions = [export_NACCategory_csv, export_NACCategory_xlsx]


def _export_programme_iterator(queryset):
    yield ['Programme Code','Description','Budget Type', 'Active']
    for obj in queryset:
        yield[ obj.programme_code,
               obj.programme_description,
               obj.budget_type,
               obj.active]


def export_programme_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_programme_iterator))


export_programme_xlsx.short_description = u"Export to Excel"


class ProgrammeAdmin(AdminActiveField):
    list_display = ('programme_code','programme_description','budget_type', 'active')
    search_fields = ['programme_code','programme_description']
    list_filter = ['budget_type','active']

    def get_readonly_fields(self, request, obj=None):
        return ['programme_code','programme_description','budget_type', 'created', 'updated'] # don't allow to edit the code

    def get_fields(self, request, obj=None):
        return ['programme_code','programme_description','budget_type', 'active', 'created', 'updated']

    actions = [export_programme_xlsx]



admin.site.register(Analysis1,Analysis1Admin)
admin.site.register(Analysis2,Analysis2Admin)
admin.site.register(NaturalCode,NaturalCodeAdmin)
admin.site.register(ExpenditureCategory, ExpenditureCategoryAdmin)
admin.site.register(NACCategory,NACCategoryAdmin)
admin.site.register(CommercialCategory)
admin.site.register(ProgrammeCode, ProgrammeAdmin)