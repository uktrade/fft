#!/usr/bin/env bash

echo "Running post build script"
pip install -r requirements.txt
npm ci
npm run build

python manage.py compilescss --settings=config.settings.build
python manage.py collectstatic --settings=config.settings.build --noinput
