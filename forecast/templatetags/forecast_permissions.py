from django import template

from guardian.shortcuts import get_objects_for_user

register = template.Library()


@register.simple_tag
def has_edit_permission(user):
    cost_centres = get_objects_for_user(
        user,
        "costcentre.change_costcentre",
    )

    if cost_centres:
        return True

    return False
