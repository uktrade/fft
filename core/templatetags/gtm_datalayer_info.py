import json

from django import template
from django.utils.html import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def get_initial_page_data(context) -> str:
    initial_page_data = {}

    if request := context.get("request"):
        initial_page_data["user_id"] = str(request.user.username)

    return mark_safe(json.dumps(initial_page_data))
