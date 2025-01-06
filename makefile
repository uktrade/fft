SHELL := /bin/bash
APPLICATION_NAME="Financial Forecast Tool"

.PHONY: help test setup
help: # List commands and their descriptions
	@grep -E '^[a-zA-Z0-9_-]+: # .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ": # "; printf "\n\033[93;01m%-30s %-30s\033[0m\n\n", "Command", "Description"}; {split($$1,a,":"); printf "\033[96m%-30s\033[0m \033[92m%s\033[0m\n", a[1], $$2}'

build: # Build the docker images for the project
	docker compose build

up: # Start the project
	docker compose up

up-dev: # Start the project
	docker compose --profile dev up
up-detatched: # Start the project in detached mode
	docker compose up -d

down: # Stop the project
	docker compose down

# Run a command in a new container
run = docker compose run --rm

# Run a command in a new container without starting linked services
run-no-deps = $(run) --no-deps

# Run a command in an existing container
exec = docker compose exec

# Run on existing container if available otherwise a new one
web := ${if $(shell docker ps -q -f name=web),$(exec) web,$(run) web}
db := ${if $(shell docker ps -q -f name=db),$(exec) db,$(run) db}

run-host = poetry run

manage = python manage.py

create-stub-data: # Create stub data for testing
	make migrate
	$(web) $(manage) set_current_year
	$(web) $(manage) create_stub_data All
	$(web) $(manage) create_stub_forecast_data
	$(web) $(manage) create_stub_future_forecast_data
	$(web) $(manage) create_data_lake_stub_data
	$(web) $(manage) populate_gift_hospitality_table
	$(web) $(manage) loaddata test_payroll_data
	$(web) $(manage) create_test_user --password=password

setup: # Set up the project from scratch
	make down
	make create-stub-data
	$(web) $(manage) create_test_user --password=password
	$(web) $(manage) create_test_user --email=finance-admin@test.com --group="Finance Administrator" --password=password  # /PS-IGNORE
	$(web) $(manage) create_test_user --email=finance-bp@test.com --group="Finance Business Partner/BSCE" --password=password  # /PS-IGNORE
	make up

gift-hospitality-table: # Populate gift hospitality table
	$(web) $(manage) populate_gift_hospitality_table

shell: # Open the web container Python/Django shell
	$(web) $(manage) shell_plus

bdd: # Run BDD tests
	$(exec) -T web $(manage) behave $(feature) --settings=config.settings.bdd --no-capture

elevate: # Elevate SSO user permissions
	$(web) $(manage) elevate_sso_user_permissions

collectstatic: # Run Django collectstatic
	$(web) $(manage) collectstatic

bash: # Open the web container bash
	$(web) bash

requirements: # Generate requirements.txt
	poetry export --with prod --without-hashes --output requirements.txt

test: # Run tests
	$(web) pytest $(test)

test-ci: # Run tests with settings for CI
	$(web) pytest --random-order -n 4 -v

superuser: # Create superuser
	$(web) $(manage) createsuperuser

# Formatting
black-check: # Run black-check
	$(run-host) black --check .

black: # Run black
	$(run-host) black .

isort-check: # Run isort-check
	$(run-host) isort --check .

isort: # Run isort
	$(run-host) isort .

ruff-check: # Run ruff in check mode
	$(run-host) ruff check

ruff: # Run ruff 
	$(run-host) ruff check --fix .

prettier-check:
	npx prettier . --check

prettier:
	npx prettier . --write

check: # Run formatters to see if there are any errors
	make ruff-check
	make black-check
	make isort-check
	make prettier-check

fix: # Run formatters to fix any issues that can be fixed automatically
	make ruff
	make black
	make isort
	make prettier

# Front End
webpack: # Run webpack
	npm run dev

# DB
migrations: # Create needed migrations
	$(web) $(manage) makemigrations

check-migrations: # Check if there are needed migrations
	$(web) $(manage) makemigrations --check

migrate: # Run migrations against the local db
	$(web) $(manage) migrate

empty-migration: # Create an empty migration
	$(web) $(manage) makemigrations $(app) --empty --name=$(name)

db-reset: # Reset the database
	docker compose stop db
	docker compose rm -f db
	docker compose up -d db

db-init: create-stub-data # Initialise the database

db-shell: # Open the database container postgres shell
	$(db) psql -U postgres

DUMP_NAME = local

db-dump: # Dump the current database, use `DUMP_NAME` to change the name of the dump
	@PGPASSWORD='postgres' pg_dump postgres -U postgres -h localhost -p 5432 -O -x -c -f ./.dumps/$(DUMP_NAME).dump

db-from-dump: # Load a dumped database, use `DUMP_NAME` to change the name of the dump
	@PGPASSWORD='postgres' psql -h localhost -U postgres postgres -f ./.dumps/$(DUMP_NAME).dump


# platform-helper

# target specific variables (not global)
codebase-build codebase-deploy copilot-ssh: profile = "fft"
codebase-build codebase-deploy copilot-ssh: app = "fft"
codebase-build codebase-deploy copilot-ssh: codebase = "fft"
codebase-build codebase-deploy: commit := $(shell git rev-parse --short HEAD)
codebase-deploy: env = "dev"
copilot-ssh: name = "web"

codebase-build:
	AWS_PROFILE=$(profile) platform-helper codebase build --app $(app) --codebase $(codebase) --commit $(commit)

codebase-deploy:
	AWS_PROFILE=$(profile) platform-helper codebase deploy --app $(app) --codebase $(codebase) --commit $(commit) --env $(env)

copilot-ssh:
	AWS_PROFILE=$(profile) copilot svc exec --app $(app) --env $(env) --name $(name) --command 'launcher bash'
