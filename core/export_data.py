from core.exportutils import get_fk_value


def export_logentry_iterator(queryset):
    yield ["Action Time", "Content Type", "Action Flag", "Change Message"]
    for obj in queryset:
        yield [
            obj.action_time,
            get_fk_value(obj.content_type, "name"),
            obj.action_flag,
            obj.change_message
        ]
