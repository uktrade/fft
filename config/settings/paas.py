from dbt_copilot_python.network import setup_allowed_hosts
from dbt_copilot_python.utility import is_copilot

from .base import *


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# TODO (DWPF-1696): Remove ECS formatter
LOGGING["handlers"]["console"]["formatter"] = "ecs"

if is_copilot():
    ALLOWED_HOSTS = setup_allowed_hosts(ALLOWED_HOSTS)

    LOGGING["handlers"]["console"]["formatter"] = "asim"
