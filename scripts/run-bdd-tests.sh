#!/bin/bash

set -ex

mv .env .env.local
cp .env.ci .env

npm run build

docker compose restart web celery

docker compose exec web python manage.py collectstatic --no-input

docker compose up -d chrome

docker compose exec --no-TTY web python manage.py behave --settings=config.settings.bdd --no-capture

rm .env
mv .env.local .env
