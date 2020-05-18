from django import template

from gifthospitality.utils.access_helpers import (
    can_view_all_gifthospitality as can_view_gifthospitality_helper,
)

register = template.Library()


@register.simple_tag
def is_gifthospitality_user(user):
    return can_view_gifthospitality_helper(user)


@register.simple_tag
def can_view_all_gifthospitality(user):
    return can_view_gifthospitality_helper(user)


@register.simple_tag
def can_view_gifthospitality(user):
    return can_view_gifthospitality_helper(user)
