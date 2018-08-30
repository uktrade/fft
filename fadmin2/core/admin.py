from django.contrib import admin
from django.contrib.admin.models import DELETION
from django.utils.html import escape
from django.urls import reverse
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

from .models import AdminInfo, EventLog


class LogEntryAdmin(admin.ModelAdmin):
    """ Display the Admin log in the Admin interface"""
    date_hierarchy = 'action_time'

    # make everything readonly
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


class AdminActiveField(admin.ModelAdmin):
    """Admin class including the handling for the active flag """

    def change_active_flag(self, request, queryset, new_active_value):
        if new_active_value is True:
            msg = 'activated'
        else:
            msg = 'deactivated'
        q = queryset.filter(active=not new_active_value)
        ct = ContentType.objects.get_for_model(queryset.model)  # for_model --> get_for_model
        for obj in q:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message=str(obj) + ' ' + msg)
        rows_updated = q.update(active=new_active_value)
        if rows_updated == 1:
            message_bit = "1 {} was".format(queryset.model._meta.verbose_name)
        else:
            message_bit = "{} {} were ".format(rows_updated, queryset.model._meta.verbose_name_plural)
        self.message_user(request, "{} successfully {}.".format(message_bit, msg))

    def make_inactive(self, request, queryset):
        self.change_active_flag(request, queryset, False)

    def make_active(self, request, queryset):
        self.change_active_flag(request, queryset, True)

    make_inactive.short_description = u"Deactivate the selected object(s)"
    make_active.short_description = u"Activate the selected object(s)"
    actions = [make_inactive, make_active]


class AdminEditOnly(admin.ModelAdmin):
    """Admin class removing edit on the model useful for structures created elsewhere, where DIT wants to add useful tags """

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


class AdminreadOnly(AdminEditOnly):
    """Admin class removing create/edit/delete on the model useful for structures created elsewhere and not changeable by DIT, like Treasury """

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.readonly_fields = [field.name for field in obj.__class__._meta.fields]
        return self.readonly_fields


admin.site.register(AdminInfo)
