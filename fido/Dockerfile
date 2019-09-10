FROM python:3.6
WORKDIR /root/fido
ADD . /root/fido/

RUN rm -f .environ \
    && rm -rf .git/ \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements/production.txt

CMD python manage.py migrate && gunicorn fido.wsgi:application --bind 0.0.0.0
