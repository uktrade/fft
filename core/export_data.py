from core.utils.export_helpers import get_fk_value


def export_logentry_iterator(queryset):
    yield ["Action Time", "User", "Content Type",
           "Action Flag", "ID", "ID Name", "Change Message"]
    for obj in queryset:
        yield [
            obj.action_time,
            obj.user.email,
            get_fk_value(obj.content_type, "name"),
            obj.action_flag,
            obj.object_id,
            obj.object_repr,
            obj.change_message
        ]
