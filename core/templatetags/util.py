from copy import copy

from django import template


register = template.Library()


@register.filter('startswith')
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
