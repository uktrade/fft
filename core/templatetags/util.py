from copy import copy

from django import template


register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    return text.startswith(starts)


@register.filter
def instances_and_widgets(bound_field):
    """Allows the access of both model instance
    and form widget in template"""
    instance_widgets = []
    index = 0
    for instance in bound_field.field.queryset.all():
        widget = copy(bound_field[index])
        instance_widgets.append((instance, widget))
        index += 1
    return instance_widgets


@register.simple_tag
def has_end_of_month_archive_permissions(user):
    if user.is_superuser or user.groups.filter(name="Finance Administrator"):
        return True


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary.

    Examples:
        `{{ dict_obj|get_item:key }}`
    """
    if not isinstance(dictionary, dict):
        return ""
    return dictionary.get(key, "")
