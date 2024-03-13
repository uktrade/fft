import json
import os
from copy import copy

from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

CONTEXT_KEY = "FFT_BREADCRUMB_LINKS"

register = template.Library()


@register.simple_tag(takes_context=True)
def append_breadcrumb(context, label, viewname, args, kwargs):
    breadcrumbs = context["request"].META.get(CONTEXT_KEY, [])
    breadcrumbs.append((label, viewname, args, kwargs))
    context["request"].META[CONTEXT_KEY] = breadcrumbs


@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, *args):
    breadcrumbs = context["request"].META.get(CONTEXT_KEY, [])
    return "FIXME!"  # Use the "breadcrumbs.html" template to render the breadcrumbs


@register.simple_tag(takes_context=True)
def breadcrumb(context, label, viewname, *args, **kwargs):
    """
    Add link to list of breadcrumbs, usage:

    {% load bubbles_breadcrumbs %}
    {% breadcrumb "Home" "index" %}

    Remember to use it inside {% block %} with {{ block.super }} to get all
    parent breadcrumbs.

    :param label: Breadcrumb link label.
    :param viewname: Name of the view to link this breadcrumb to, or Model
                     instance with implemented get_absolute_url().
    :param args: Any arguments to view function.
    """
    append_breadcrumb(context, _(escape(label)), viewname, args, kwargs)
    return ""
