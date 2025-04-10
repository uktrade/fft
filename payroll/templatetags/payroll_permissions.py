from django import template

import payroll.services.payroll as payroll_service


register = template.Library()


@register.simple_tag
def can_access_edit_payroll(user):
    return payroll_service.can_access_edit_payroll(user)
