create-sub-data:
	docker-compose run fido python manage.py migrate
	docker-compose run fido python manage.py create_stub_data All
	docker-compose run fido python manage.py create_stub_forecast_data
	docker-compose run fido python manage.py create_test_user

setup-new-test-env:
	docker-compose down
	docker-compose run fido python manage.py migrate
	docker-compose run fido python manage.py create_stub_data All
	docker-compose run fido python manage.py create_stub_forecast_data
	docker-compose run fido python manage.py populate_gift_hospitality_table
	docker-compose run fido python manage.py create_test_user --password=password
	docker-compose run fido python manage.py create_test_user --email=finance-admin@test.com --group="Finance Administrator" --password=password
	docker-compose run fido python manage.py create_test_user --email=finance-bp@test.com --group="Finance Business Partner/BSCE" --password=password

makemigrations:
	docker-compose run fido python manage.py makemigrations

migrate:
	docker-compose run fido python manage.py migrate

compilescss:
	docker-compose run fido python manage.py compilescss

test:
	docker-compose run fido python manage.py test $(test)

shell:
	docker-compose run fido python manage.py shell

flake8:
	docker-compose run fido flake8 $(file)

bdd:
	npm run bdd; \
	docker-compose exec fido sh -c "python manage.py behave $(feature) --settings=config.settings.bdd --no-capture"

up:
	docker-compose up

build:
	docker-compose build

elevate:
	docker-compose run fido python manage.py elevate_sso_user_permissions

collectstatic:
	docker-compose run fido python manage.py collectstatic

bash:
	docker-compose run fido bash

dev-requirements:
	pip-compile --output-file requirements/base.txt requirements.in/base.in
	pip-compile --output-file requirements/dev.txt requirements.in/dev.in

production-requirements:
	pip-compile --output-file requirements/base.txt requirements.in/base.in
	pip-compile --output-file requirements/production.txt requirements.in/production.in
