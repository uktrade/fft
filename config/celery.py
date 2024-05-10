# fido/fido/celery.py
# https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
import os

from celery import Celery
from dbt_copilot_python.celery_health_check import healthcheck
from dbt_copilot_python.utility import is_copilot


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

celery_app = Celery("DjangoCelery")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

if is_copilot():
    celery_app = healthcheck.setup(celery_app)


@celery_app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
