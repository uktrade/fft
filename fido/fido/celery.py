# fadmin2/fadmin2/celery.py
# https://stackabuse.com/asynchronous-tasks-in-django-with-redis-and-celery/
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fadmin2.settings')

celery_app = Celery('DjangoCelery')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

