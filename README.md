# FFT (Financial Forecast Tool)

## Requirements

- [Docker](https://www.docker.com/) - To get the project running locally.
- Access to Vault. (dit/finance/)
- SSO Access to Finance Admin Tool[non prod].

## Initial Setup

First you will need to make a copy of the `.env.example` file and rename it to `.env`. This file contains most of the environment variables that the project needs to run.

```bash
cp .env.example .env
```

To get `AUTHBROKER_CLIENT_ID`, `AUTHBROKER_CLIENT_SECRET` and `AUTHBROKER_URL` variables, you need to have access to `dit/finance/` directory in Vault. You can get access to this directory by asking SRE to add you to the finance team on GitHub.

Make sure your SSO profile has access rights for FFT on [dev](https://fft.trade.dev.uktrade.digital) environment. If not, please contact SRE for access to Finance Admin Tool[non prod].

In your terminal run `make setup` command from the project’s root directory.

```bash
make setup
```

This command will run the initial migrations, create stub data and a test user.

In another terminal run `npm run dev` to load the node packages for the frontend.

```bash
npm run dev
```

### Local Development

If you can connect to the dev environment but still have issues such as; `403 - Forbidden Error` on your local, there are few steps you can follow to resolve this:

- Using dev tools on your browser, go to Application tab and clear data for Local Storage, Session Storage and Cookies.

- If the problem persists you may need to temporarily pause your VPN while you work on FFT on your local.

You can access the webserver on port `8000`:

- [http://localhost:8000/](http://localhost:8000/)

### Access to Admin Tool

You need to run `make elevate` command to elevate your user permissions in order to access the admin tool.

```bash
make elevate
```

After running this command refresh the FFT page and you will have the admin privileges.

### Running docker-compose run with port access

```
docker-compose run --service-ports
```

### Important notes on design

We use Django Guardian for model instance level permissions https://github.com/django-guardian/django-guardian

Django Guardian **should not be used directly**. There is a set of wrapper functions in _forecast.permission_shortcuts_

These add an additional permission check for the user being able to view forecasts at all.

### Creating data/non-auto migrations

When adding data or non-auto generated migrations, please use the convention:

```
[number]_data_[date]_[time]
```

for example:

```
0004_data_20200501_1345
```

### Running manage.py on an app droplet

```
/home/vcap/deps/1/bin/python3.6 ~/app/manage.py
```

### Running BDD tests

## Run BDD front end from host machine

```
npm run bdd
``

## SSH into web container

```

docker-compose exec web bash

```

## Run BDD tests

```

python manage.py behave --settings=config.settings.bdd

```

### Notes

In order to get the node docker container working, this guide was followed: https://jdlm.info/articles/2019/09/06/lessons-building-node-app-docker.html

### Product URLs

#### Dev URL

https://fft.trade.dev.uktrade.digital/core/

#### Production URL

https://fft.trade.gov.uk/core/

### Managing user permissions

4 management commands have been added to make dealing with user cost centre easier:

- add_user_to_cost_centre
- cost_centre_users
- remove_user_from_cost_centre
- user_permissions

The names of the management commands denote their function.

### Permissions within the system

#### Any logged in SSO user

- Access Chart of Account Gifts and Hospitality Register

#### Specific permissions

- Upload budget and Oracle actuals file
- Download Oscar report file
- View forecast (permission to view all forecast data)
- Edit 1 - n cost centres (specific user can edit cost centre data)

#### Migrating to new user model (to be removed once complete)

- Take the system off line
- Add username field to HistoricalUser table (max length 150, allow null)
- Amend the custom_usermodel table to be the same as the new User app one
- Add the user app initial migration to the list of django migrations that have been run
- Deploy new codebase
```
