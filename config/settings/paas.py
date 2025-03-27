from dbt_copilot_python.network import setup_allowed_hosts

from .base import *


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = setup_allowed_hosts(ALLOWED_HOSTS)

LOGGING["handlers"]["console"]["formatter"] = "asim"
