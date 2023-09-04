#!/usr/bin/env bash

echo "Running post build script"
pip install -r requirements.txt

python manage.py compilescss --settings=config.settings.build
python manage.py collectstatic --settings=config.settings.build --noinput
