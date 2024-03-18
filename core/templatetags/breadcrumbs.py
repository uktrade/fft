from django import template
from django.urls import NoReverseMatch, Resolver404, resolve, reverse
from django.utils.encoding import smart_str
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
    if not breadcrumbs:
        return ""

    links = []

    for label, viewname, view_args, view_kwargs in breadcrumbs:
        try:
            try:
                current_app = context["request"].resolver_match.namespace
            except AttributeError:
                try:
                    resolver_match = resolve(context["request"].path)
                    current_app = resolver_match.namespace
                except Resolver404:
                    current_app = None
            url = reverse(
                viewname=viewname,
                args=view_args,
                kwargs=view_kwargs,
                current_app=current_app,
            )
        except NoReverseMatch:
            url = viewname
        links.append((url, smart_str(label) if label else label))

    context = {
        "breadcrumbs": links,
        "breadcrumbs_total": len(links),
    }
    return mark_safe(template.loader.render_to_string("breadcrumbs.html", context))


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
