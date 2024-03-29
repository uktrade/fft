import logging
import sys

import requests
from django_log_formatter_ecs import ECSFormatter

from .base import *  # noqa


CAN_ELEVATE_SSO_USER_PERMISSIONS = True
CAN_CREATE_TEST_USER = True

FRONT_END_SERVER = env(
    "FRONT_END_SERVER",
    default="http://localhost:3000",
)

AUTHENTICATION_BACKENDS += [
    "user.backends.CustomAuthbrokerBackend",
]

ASYNC_FILE_UPLOAD = False

LOG_TO_ELK = env.bool("LOG_TO_ELK", default=False)
ELK_ADDRESS = env("ELK_ADDRESS", default=None)

if LOG_TO_ELK:

    class LogstashHTTPHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)

            return requests.post(
                ELK_ADDRESS,
                data="{}".format(log_entry),
                headers={"Content-type": "application/json"},
            ).content

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "ecs_formatter": {
                "()": ECSFormatter,
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
            "logstash": {
                "()": LogstashHTTPHandler,
                "formatter": "ecs_formatter",
            },
        },
        "loggers": {
            "django.request": {
                "handlers": [
                    "stdout",
                    "logstash",
                ],
                "level": "WARNING",
                "propagate": True,
            },
        },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "root": {
            "handlers": ["stdout"],
            "level": os.getenv("ROOT_LOG_LEVEL", "INFO"),
        },
        "loggers": {
            "django": {
                "handlers": [
                    "stdout",
                ],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": True,
            },
            "forecast.import_csv": {
                "handlers": [
                    "stdout",
                ],
                "level": "INFO",
                "propagate": True,
            },
        },
    }
