FROM python:3

WORKDIR /root/
ADD fadmin2 fadmin2
ADD requirements.txt fadmin2/requirements.txt

WORKDIR /root/fadmin2
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["gunicorn","fadmin2.wsgi:application","--bind","0.0.0.0"]
