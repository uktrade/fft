from django.contrib import admin

from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from core.exportutils import export_to_csv, export_to_excel
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


def make_cc_inactive(modeladmin, request, queryset):
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


def make_cc_active(modeladmin, request, queryset):
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
make_cc_inactive.short_description = u"Lock the selected Cost Centres"
make_cc_active.short_description = u"Unlock the selected Cost Centres"

# Displays extra fields in the list of cost centres
class CostCentreAdmin(admin.ModelAdmin):
    list_display = ('cost_centre_code', 'cost_centre_name', 'directorate', 'group', 'active')

    def directorate(self, instance): # required to display the filed from a foreign key
        return instance.directorate.directorate_code + ' - ' +instance.directorate.directorate_name

    def group(self, instance):
        return instance.directorate.group.group_code + ' - ' + instance.directorate.group.group_name

    # different fields visible if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['cost_centre_code', 'created', 'updated'] # don't allow to edit the code
        else:
            return ['created', 'updated']

    # different fields visible if updating or creating the object
    def get_fields(self, request, obj=None):
        if obj:
            return ['cost_centre_code', 'cost_centre_name', 'directorate', 'active', 'created', 'updated']
        else:
            return ['cost_centre_code', 'cost_centre_name', 'directorate', 'active']

    directorate.admin_order_field = 'directorate__directorate_name'  # use __ to define a table field relationship
    group.admin_order_field = 'directorate__group__group_name'  # use __ to define a table field relationship

    search_fields = ['cost_centre_code']
    list_filter = ['active','directorate__directorate_name','directorate__group__group_name']
    actions = [export_cc_csv, export_cc_xlsx, make_cc_inactive,make_cc_active] # new action to export to csv and xlsx


class DirectorateAdmin(admin.ModelAdmin):
    list_display = ('directorate_code','directorate_name', 'dgroup_name')

    def dgroup_name(self, instance):
        return instance.group.group_code + ' - ' + instance.group.group_name

    dgroup_name.admin_order_field = 'group__group_name' # use __ to define a table field relationship


admin.site.register(CostCentre, CostCentreAdmin)
admin.site.register(DepartmentalGroup)
admin.site.register(Directorate, DirectorateAdmin)

admin.site.register(Programme)