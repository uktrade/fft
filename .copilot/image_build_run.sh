#!/usr/bin/env bash

# Exit early if something goes wrong
set -ex

# Add commands below to run inside the container after all the other buildpacks have been applied

# Create .env file from .env.ci file with comments stripped out
grep -v '^#' .env.ci > .env

# Set export all variables
set -o allexport
# Source the .env file
# shellcheck source=/dev/null
. ./.env
# Unset exporting all variables
set +o allexport

python manage.py collectstatic --noinput
