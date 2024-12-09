#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

# Add commands below to run inside the container after all the other buildpacks have been applied
export DJANGO_SETTINGS_MODULE=config.settings.prod

python manage.py collectstatic --noinput
