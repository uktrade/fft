from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from core.exportutils import export_to_csv, export_to_excel, generic_export_to_csv, generic_export_to_excel
from core.myutils import AdminreadOnly

from .models import Analysis1, Analysis2, NaturalCode, NACDashboardGrouping, NACCategory


EXPORT_NAC_ITERATOR_HEADERS=['Level 6','Level 6 Description', 'DIT Use', 'Level 5', 'Level 5 Description','Category','Dashboard Group']

def _export_nac_iterator(queryset):
    yield EXPORT_NAC_ITERATOR_HEADERS
    for obj in queryset:
        yield[obj.natural_account_code,
            obj.natural_account_code_description,
            obj.used_by_DIT,
            obj.account_L5_code,
            obj.account_L5_code.account_l5_long_name,
            obj.NAC_category.NAC_category_description,
            obj.dashboard_grouping.grouping_description,
            obj.account_L5_code.economic_budget_code,
            obj.account_L5_code.economic_budget_code,
            obj.account_L5_code.usage_code]


def export_nac_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_nac_iterator))


def export_nac_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_nac_iterator))


export_nac_xlsx.short_description = u"Export to XLSX"
export_nac_csv.short_description = u"Export to csv"

    
class NaturalCodeAdmin(AdminreadOnly):
    def get_readonly_fields(self, request, obj=None):
        return ['natural_account_code', 'natural_account_code_description', 'account_L5_code'] # don't allow to edit the code

    search_fields = ['natural_account_code']
    list_filter = ['used_by_DIT','NAC_category__NAC_category_description', 'dashboard_grouping__grouping_description']
    actions = [export_nac_csv, export_nac_xlsx] # new action to export to csv and xlsx


def export_analysis1_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_analysis1_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))



class Analysis1Admin(AdminreadOnly):
    search_fields = ['analysis1_description']
    actions = [export_analysis1_csv, export_analysis1_xlsx] # new action to export to csv and xlsx


def export_analysis2_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_analysis2_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class Analysis2Admin(AdminreadOnly):
    search_fields = ['analysis2_description']
    actions = [export_analysis2_csv, export_analysis2_xlsx] # new action to export to csv and xlsx



def export_NACDashboardGrouping_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_NACDashboardGrouping_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class NACDashboardGroupingAdmin(admin.ModelAdmin):
    search_fields = ['grouping_description']
    actions = [export_NACDashboardGrouping_csv, export_NACDashboardGrouping_xlsx] # new action to export to csv and xlsx


def export_NACCategory_csv(modeladmin, request, queryset):
    return(generic_export_to_csv(queryset))


def export_NACCategory_xlsx(modeladmin, request, queryset):
    return(generic_export_to_excel(queryset))


class NACCategoryAdmin(admin.ModelAdmin):
     actions = [export_NACCategory_csv, export_NACCategory_xlsx] # new action to export to csv and xlsx


admin.site.register(Analysis1,Analysis1Admin)
admin.site.register(Analysis2,Analysis2Admin)
admin.site.register(NaturalCode,NaturalCodeAdmin)
admin.site.register(NACDashboardGrouping, NACDashboardGroupingAdmin)
admin.site.register(NACCategory,NACCategoryAdmin)
