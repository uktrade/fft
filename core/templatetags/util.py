import json
import os
from copy import copy

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def render_front_end_script():
    if settings.DEBUG:
        return mark_safe(
            '<script '
            'type="text/javascript" '
            f'src="/{settings.FRONT_END_SERVER}/static/js/bundle.js">'
            '</script>'
        )
    else:
        assets_manifest_path = os.path.join(
            settings.BASE_DIR, "front_end/build/asset-manifest.json"
        )
        with open(assets_manifest_path) as assets_manifest:
            asset_json = json.load(assets_manifest)
            scripts = []

            # Check for legacy format asset manifest
            if "entrypoints" in asset_json:
                for script_path in asset_json["entrypoints"]:
                    scripts.append(script_path)
            else:
                for key in asset_json:
                    if asset_json[key].endswith(".js"):
                        scripts.append(asset_json[key])

            return mark_safe(
                ''.join([
                    '<script type="text/javascript" src="/{}"></script>'.format(
                        script
                    ) for script in scripts
                ])
            )


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
