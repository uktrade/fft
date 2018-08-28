from django.contrib import admin


from .models import AdminInfo, EventLog


from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse


class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

#    readonly_fields = LogEntry._meta.get_all_field_names()
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag_',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def action_flag_(self, obj):
        flags = {
            1: "Addition",
            2: "Changed",
            3: "Deleted",
        }
        return flags[obj.action_flag]

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'


admin.site.register(LogEntry, LogEntryAdmin)







class AdminreadOnly(admin.ModelAdmin):
    """Admin class removing create/edit/delete on the model useful for structures created elsewhere and not changeable by DIT, like Treasury """
    # different fields visible if updating or creating the object
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields

    # Remove delete from the list of action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Don't allow add
    def has_add_permission(self, request):
        return False

    # Don't allow delete
    def has_delete_permission(self, request, obj=None):
        return False

    # unfortunately, I cannot find a way to remove the 'save' button.



class AdminEditOnly(admin.ModelAdmin):
    """Admin class removing edit on the model useful for structures created elsewhere, where DIT wants to add useful tags """
    # different fields visible if updating or creating the object
     # Remove delete from the list of action
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Don't allow add
    def has_add_permission(self, request):
        return False

    # Don't allow delete
    def has_delete_permission(self, request, obj=None):
        return False

    # unfortunately, I cannot find a way to remove the 'save' button.

admin.site.register(AdminInfo)
admin.site.register(EventLog)
