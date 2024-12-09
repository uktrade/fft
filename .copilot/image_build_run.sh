#!/usr/bin/env bash

# Exit early if something goes wrong
set -ex

# Add commands below to run inside the container after all the other buildpacks have been applied

# Set export all variables
set -o allexport
# Source .env.ci as the env file for building
# shellcheck source=/dev/null
. ./.env.ci
# Unset export all variables
set +o allexport

python manage.py collectstatic --noinput
