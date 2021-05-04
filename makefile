SHELL := /bin/bash
APPLICATION_NAME="Financial Forecast Tool"

# Colour coding for output
COLOUR_NONE=\033[0m
COLOUR_GREEN=\033[32;01m
COLOUR_YELLOW=\033[33;01m
COLOUR_RED='\033[0;31m'

.PHONY: help test
help:
	@echo -e "$(COLOUR_GREEN)|--- $(APPLICATION_NAME) ---|$(COLOUR_NONE)"
	@echo -e "$(COLOUR_YELLOW)make build$(COLOUR_NONE) : Run docker-compose build"
	@echo -e "$(COLOUR_YELLOW)make up$(COLOUR_NONE) : Run docker-compose up"
	@echo -e "$(COLOUR_YELLOW)make down$(COLOUR_NONE) : Run docker-compose down"
	@echo -e "$(COLOUR_YELLOW)make create-stub-data$(COLOUR_NONE) : Create dataset for use with local development"
	@echo -e "$(COLOUR_YELLOW)make first-use$(COLOUR_NONE) : Create development environment and set up with test data and test users"
	@echo -e "$(COLOUR_YELLOW)make gift-hospitality-table$(COLOUR_NONE) : Create gifts and hospitality data"
	@echo -e "$(COLOUR_YELLOW)make migrations$(COLOUR_NONE) : Run Django makemigrations"
	@echo -e "$(COLOUR_YELLOW)make migrate$(COLOUR_NONE) : Run Django migrate"
	@echo -e "$(COLOUR_YELLOW)make compilescss$(COLOUR_NONE) : Compile SCSS into CSS"
	@echo -e "$(COLOUR_YELLOW)make shell$(COLOUR_NONE) : Run a Django shell"
	@echo -e "$(COLOUR_YELLOW)make flake8$(COLOUR_NONE) : Run flake8 checks"
	@echo -e "$(COLOUR_YELLOW)make bdd$(COLOUR_NONE) : Run Django BDD tests"
	@echo -e "$(COLOUR_YELLOW)make elevate$(COLOUR_NONE) : Elevate user permission to superuser"
	@echo -e "$(COLOUR_YELLOW)make collectstatic$(COLOUR_NONE) : Run Django BDD tests"
	@echo -e "$(COLOUR_YELLOW)make bash$(COLOUR_NONE) : Start a bash session on the application container"
	@echo -e "$(COLOUR_YELLOW)make all-requirements$(COLOUR_NONE) : Generate pip requirements files"
	@echo -e "$(COLOUR_YELLOW)make test$(COLOUR_NONE) : Run Django tests"
	@echo -e "$(COLOUR_YELLOW)make pytest$(COLOUR_NONE) : Run pytest"
	@echo -e "$(COLOUR_YELLOW)make black$(COLOUR_NONE) : Run black formatter"

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

create-stub-data:
	docker-compose --rm run fido python manage.py migrate
	docker-compose --rm run fido python manage.py create_stub_data All
	docker-compose --rm run fido python manage.py create_stub_forecast_data
	docker-compose --rm run fido python manage.py create_test_user

first-use:
	docker-compose down
	docker-compose run --rm fido python manage.py migrate
	docker-compose run --rm fido python manage.py create_stub_data All
	docker-compose run --rm fido python manage.py create_stub_forecast_data
	docker-compose run --rm fido python manage.py populate_gift_hospitality_table
	docker-compose run --rm fido python manage.py create_test_user --password=password
	docker-compose run --rm fido python manage.py create_test_user --email=finance-admin@test.com --group="Finance Administrator" --password=password
	docker-compose run --rm fido python manage.py create_test_user --email=finance-bp@test.com --group="Finance Business Partner/BSCE" --password=password

gift-hospitality-table:
	docker-compose run fido python manage.py populate_gift_hospitality_table

migrations:
	docker-compose run --rm fido python manage.py makemigrations

migrate:
	docker-compose run --rm fido python manage.py migrate

compilescss:
	docker-compose run --rm fido python manage.py compilescss

shell:
	docker-compose run --rm fido python manage.py shell

flake8:
	docker-compose run --rm fido flake8 $(file)

bdd:
	npm run bdd; \
	docker-compose exec fido sh -c "python manage.py behave $(feature) --settings=config.settings.bdd --no-capture"

elevate:
	docker-compose run --rm fido python manage.py elevate_sso_user_permissions

collectstatic:
	docker-compose run --rm fido python manage.py collectstatic

bash:
	docker-compose run --rm fido bash

all-requirements:
	docker-compose run --rm fido pip-compile --output-file requirements/base.txt requirements.in/base.in
	docker-compose run --rm fido pip-compile --output-file requirements/dev.txt requirements.in/dev.in
	docker-compose run --rm fido pip-compile --output-file requirements/prod.txt requirements.in/prod.in

test:
	docker-compose run --rm fido python manage.py test $(test)

pytest:
	docker-compose run --rm fido pytest -raP --capture=sys --ignore=node_modules --ignore=front_end --ignore=features --ignore=staticfiles -n 4

black:
	docker-compose run --rm fido black .

superuser:
	docker-compose run --rm fido python manage.py createsuperuser

