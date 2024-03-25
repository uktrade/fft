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

up-detatched:
	docker-compose up -d

down:
	docker-compose down

create-stub-data:
	docker-compose --rm run web python manage.py migrate
	docker-compose --rm run web python manage.py create_stub_data All
	docker-compose --rm run web python manage.py create_stub_forecast_data
	docker-compose --rm run web python manage.py create_test_user

first-use:
	docker-compose down
	docker-compose run --rm web python manage.py migrate
	docker-compose run --rm web python manage.py create_stub_data All
	docker-compose run --rm web python manage.py create_stub_future_forecast_data
	docker-compose run --rm web python manage.py create_stub_forecast_data
	docker-compose run --rm web python manage.py create_stub_future_forecast_data
	docker-compose run --rm web python manage.py create_data_lake_stub_data
	docker-compose run --rm web python manage.py populate_gift_hospitality_table
	docker-compose run --rm web python manage.py create_test_user --password=password
	docker-compose run --rm web python manage.py create_test_user --email=finance-admin@test.com --group="Finance Administrator" --password=password  # /PS-IGNORE
	docker-compose run --rm web python manage.py create_test_user --email=finance-bp@test.com --group="Finance Business Partner/BSCE" --password=password  # /PS-IGNORE
	docker-compose up

gift-hospitality-table:
	docker-compose run web python manage.py populate_gift_hospitality_table

migrations:
	docker-compose run --rm web python manage.py makemigrations

migrate:
	docker-compose run --rm web python manage.py migrate

shell:
	docker-compose run --rm web python manage.py shell

flake8:
	docker-compose run --rm web flake8 $(file)

bdd:
	docker-compose exec -T web python manage.py behave $(feature) --settings=config.settings.bdd --no-capture --no-color

elevate:
	docker-compose run --rm web python manage.py elevate_sso_user_permissions

collectstatic:
	docker-compose run --rm web python manage.py collectstatic

bash:
	docker-compose run --rm web bash

all-requirements:
	poetry export --with prod --without-hashes --output requirements.txt

test:
	docker-compose run --rm web python manage.py test $(test)

pytest:
	docker-compose run --rm web pytest --ignore=node_modules --ignore=front_end --ignore=features --ignore=staticfiles --random-order -n 4

black-check:
	docker-compose run --rm --no-deps web black --check .

black:
	docker-compose run --rm web black .

isort-check:
	docker-compose run --rm web isort --check .

isort:
	docker-compose run --rm web isort .

superuser:
	docker-compose run --rm web python manage.py createsuperuser
