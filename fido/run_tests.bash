#!/usr/bin/env bash
npm run bdd
docker-compose run fido python manage.py test
docker-compose run fido behave
