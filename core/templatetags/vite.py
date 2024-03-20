"""Template tags for the Vite integration.

Settings:
    VITE_DEV (bool): Enable dev mode (default: `False`)
    VITE_DEV_SERVER_URL (str): Dev server url (default: `"http://localhost:5173"`)
    VITE_MANIFEST_PATH (str): Path to the manifest file
"""

import json
from functools import cache
from typing import Any

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe


register = template.Library()

# https://docs.djangoproject.com/en/5.0/ref/settings/#prefixes-optional
# This needs to match the prefix given to the vite build directory entry in the
# `STATICFILES_DIR` setting.
VITE_STATICFILES_PREFIX = "vite"


@cache
def get_manifest() -> dict[str, dict[str, Any]]:
    with settings.VITE_MANIFEST_PATH.open() as f:
        manifest = json.load(f)

    return manifest


@register.simple_tag
def vite_static(filename: str) -> str:
    file = get_manifest()[filename]["file"]
    return static(f"{VITE_STATICFILES_PREFIX}/{file}")


@register.simple_tag
def vite_css(filename: str) -> str:
    if settings.VITE_DEV:
        return mark_safe(
            f'<link rel="stylesheet" href="{settings.VITE_DEV_SERVER_URL}/{filename}">'  # noqa: E501
        )

    return mark_safe(f'<link rel="stylesheet" href="{vite_static(filename)}">')


@register.simple_tag
def vite_js(filename: str) -> str:
    if settings.VITE_DEV:
        return mark_safe(
            f'<script type="module" src="{settings.VITE_DEV_SERVER_URL}/{filename}"></script>'  # noqa: E501
        )

    return mark_safe(f'<script type="module" src="{vite_static(filename)}"></script>')


# https://vitejs.dev/guide/backend-integration.html
REACT_SCRIPT = """
<script type="module">
    import RefreshRuntime from '{dev_server_url}/@react-refresh'
    RefreshRuntime.injectIntoGlobalHook(window)
    window.$RefreshReg$ = () => {{}}
    window.$RefreshSig$ = () => (type) => type
    window.__vite_plugin_react_preamble_installed__ = true
</script>
"""


@register.simple_tag
def vite_dev_client(react: bool = True) -> str:
    if not settings.VITE_DEV:
        return ""

    scripts = []

    if react:
        scripts.append(REACT_SCRIPT.format(dev_server_url=settings.VITE_DEV_SERVER_URL))

    scripts.append(
        f'<script type="module" src="{settings.VITE_DEV_SERVER_URL}/@vite/client"></script>'  # noqa: E501
    )

    return mark_safe("\n".join(scripts))
