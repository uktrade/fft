import json

from django import template
from django.utils.html import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def get_initial_page_data(context) -> str:
    request = context["request"]

    initial_page_data = {}

    initial_page_data["user_id"] = str(request.user.id)

    return mark_safe(json.dumps(initial_page_data))
