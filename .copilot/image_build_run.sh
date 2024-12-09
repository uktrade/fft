#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

export DJANGO_SETTINGS_MODULE=config.settings.prod

cp .env.ci .env

# Add commands below to run inside the container after all the other buildpacks have been applied

python manage.py collectstatic --noinput
