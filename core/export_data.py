from core.utils.export_helpers import get_fk_value


def export_logentry_iterator(queryset):
    yield ["Action Time", "User Email", "Content Type", "Action Flag", "Change Message"]
    for obj in queryset:
        yield [
            obj.action_time,
            obj.user.email,
            get_fk_value(obj.content_type, "name"),
            obj.action_flag,
            obj.change_message
        ]
