import dj_database_url
from dbt_copilot_python.database import database_url_from_env
from dbt_copilot_python.network import setup_allowed_hosts
from dbt_copilot_python.utility import is_copilot

from .base import *


# TODO (DWPF-1696): Remove ECS formatter
LOGGING["handlers"]["console"]["formatter"] = "ecs"

if is_copilot():
    ALLOWED_HOSTS = setup_allowed_hosts(ALLOWED_HOSTS)

    DATABASES["default"] = dj_database_url.config(
        default=database_url_from_env("DATABASE_CREDENTIALS")
    )

    REDIS_URL = env("REDIS_URL", default=None) + "?ssl_cert_reqs=required"

    LOGGING["handlers"]["console"]["formatter"] = "asim"
