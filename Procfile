web: python manage.py gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 300 --log-file -
worker: celery  -A config worker -l info