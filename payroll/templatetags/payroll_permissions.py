from django import template


register = template.Library()


@register.simple_tag
def can_edit_payroll(user):
    return user.is_superuser
