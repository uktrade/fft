FROM python:3

WORKDIR /root/fadmin2
ADD . /root/fadmin2/

RUN rm -f .environ \
    && rm -rf .git/ \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD python manage.py migrate && gunicorn fadmin2.wsgi:application --bind 0.0.0.0