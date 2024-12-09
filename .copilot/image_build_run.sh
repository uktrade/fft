#!/usr/bin/env bash

# Exit early if something goes wrong and 
set -ex

# Add commands below to run inside the container after all the other buildpacks have been applied
export $(grep -v '^#' .env | xargs -d '\n')

python manage.py collectstatic --noinput
