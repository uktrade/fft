import dj_database_url
from dbt_copilot_python.database import database_url_from_env
from dbt_copilot_python.network import setup_allowed_hosts
from dbt_copilot_python.utility import is_copilot

from .base import *


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "KEY_PREFIX": "cache_",
    }
}

# TODO (DWPF-1696): Remove ECS formatter
LOGGING["handlers"]["console"]["formatter"] = "ecs"

if is_copilot():
    ALLOWED_HOSTS = setup_allowed_hosts(ALLOWED_HOSTS)

    DATABASES["default"] = dj_database_url.config(
        default=database_url_from_env("DATABASE_CREDENTIALS")
    )

    CACHES["default"]["location"] = env.str("REDIS_ENDPOINT")

    CELERY_BROKER_URL = env.str("REDIS_ENDPOINT")

    LOGGING["handlers"]["console"]["formatter"] = "asim"
