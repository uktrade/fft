from django.contrib import admin

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from core.exportutils import export_to_csv, export_to_excel
from core.admin import AdminEditOnly

from payroll.models import DITPeople

from .models import DepartmentalGroup, Directorate, CostCentre, Programme


EXPORT_CC_ITERATOR_HEADERS=['Cost Centre','Cost Centre Description', 'Active', 'Directorate', 'Directorate Description','Group','Group Description']

def _export_cc_iterator(queryset):
    yield EXPORT_CC_ITERATOR_HEADERS
    for obj in queryset:
        yield[obj.cost_centre_code,
            obj.cost_centre_name,
            obj.active,
            obj.directorate.directorate_code,
            obj.directorate.directorate_name,
            obj.directorate.group.group_code,
            obj.directorate.group.group_name]


def export_cc_xlsx(modeladmin, request, queryset):
    return(export_to_excel(queryset, _export_cc_iterator))


def export_cc_csv(modeladmin, request, queryset):
    return (export_to_csv(queryset, _export_cc_iterator))


def make_inactive(modeladmin, request, queryset):
    q = queryset.filter(active=True)
    q.update(active=False)
    ct = ContentType.objects.get_for_model(queryset.model) # for_model --> get_for_model
    for obj in q:
        LogEntry.objects.log_action( # log_entry --> log_action
            user_id = request.user.id,
            content_type_id = ct.pk,
            object_id = obj.pk,
            object_repr = obj.__str__,
            action_flag = CHANGE, # actions_flag --> action_flag
            change_message = 'Locked.')


def make_active(modeladmin, request, queryset):
    q = queryset.filter(active=False)
    ct = ContentType.objects.get_for_model(queryset.model) # for_model --> get_for_model
    for obj in q:
        LogEntry.objects.log_action( # log_entry --> log_action
            user_id = request.user.id,
            content_type_id = ct.pk,
            object_id = obj.pk,
            object_repr = 'a', # obj_str gives an error
            action_flag = CHANGE, # actions_flag --> action_flag
            change_message = 'Unlocked.')
    q.update(active=True) # should I do it before or after writing to ther log?


export_cc_xlsx.short_description = u"Export to XLSX"
export_cc_csv.short_description = u"Export to csv"
make_inactive.short_description = u"Disactivate the selected object(s)"
make_active.short_description = u"Activate the selected object(s)"

# Displays extra fields in the list of cost centres
class CostCentreAdmin(admin.ModelAdmin):
    list_display = ('cost_centre_code', 'cost_centre_name', 'directorate_name', 'group_name', 'active')

    def directorate_name(self, instance): # required to display the field from a foreign key
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
            return ['cost_centre_code', 'created', 'updated'] # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['cost_centre_code', 'cost_centre_name', 'directorate', 'deputy_director', 'business_partner', 'active', 'created', 'updated']
        else:
            return ['cost_centre_code', 'cost_centre_name', 'directorate', 'deputy_director','business_partner', 'active']

    search_fields = ['cost_centre_code','cost_centre_name']
    list_filter = ('active',
                   ('directorate', RelatedDropdownFilter),
                   ('directorate__group', RelatedDropdownFilter))
    actions = [export_cc_csv, export_cc_xlsx, make_inactive, make_active] # new action to export to csv and xlsx


class DirectorateAdmin(admin.ModelAdmin):
    list_display = ('directorate_code','directorate_name', 'dgroup_name', 'director', 'active')
    search_fields = ['directorate_code','directorate_name']
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
            return ['directorate_code', 'created', 'updated'] # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['directorate_code', 'directorate_name', 'group', 'director', 'active', 'created', 'updated']
        else:
            return ['directorate_code', 'directorate_name', 'group', 'director', 'active']

    actions = [make_inactive, make_active]


class DepartmentalGroupAdmin(admin.ModelAdmin):
    list_display = ('group_code', 'group_name', 'director_general', 'active')
    search_fields = ['group_code','group_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'director_general':
            kwargs["queryset"] = DITPeople.objects.filter(isdirector=True, active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # different fields editable if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['group_code', 'created', 'updated'] # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['group_code', 'group_name', 'director_general', 'active', 'created', 'updated']
        else:
            return ['group_code', 'group_name', 'director_general', 'active']

    actions = [make_inactive, make_active] # new action to export to csv and xlsx




class ProgrammeAdmin(AdminEditOnly):
    list_display = ('programme_code','programme_description','budget_type', 'DIT_in_use')
    search_fields = ['programme_code','programme_description']
    list_filter = ['budget_type','DIT_in_use']

    def get_readonly_fields(self, request, obj=None):
        return ['programme_code','programme_description','budget_type', 'created', 'updated'] # don't allow to edit the code

    def get_fields(self, request, obj=None):
        return ['programme_code','programme_description','budget_type', 'DIT_in_use', 'created', 'updated']



admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup, DepartmentalGroupAdmin)
admin.site.register(Directorate, DirectorateAdmin)

admin.site.register(Programme, ProgrammeAdmin)