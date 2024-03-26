# FFT (Financial Forecast Tool)

## Requirements

- [docker](https://docs.docker.com/engine/install/)
- [poetry](https://python-poetry.org/docs/#installation)

## Local setup

First you will need to make a copy of the `.env.example` file and rename it to `.env`.
This file contains most of the environment variables that the project needs to run.

```bash
cp .env.example .env
```

Fill out the required variables in your `.env` file.

> [!TIP]
> For the `AUTHBROKER_CLIENT_ID`, `AUTHBROKER_CLIENT_SECRET` and `AUTHBROKER_URL`
> variables, ask a member of the team to assist you in getting the values from the dev
> environment.

In a terminal run the `make setup` command from the project’s root directory.

```bash
make setup
```

> [!NOTE]
> This command will run the initial migrations, create stub data and test users.

Open a second terminal and run `npm run dev` to load the node packages for the frontend.

```bash
npm run dev
```

You should now be able to access the application at http://localhost:8000/.

If you want full admin access, you can elevate your by running:

```bash
make elevate
```

> [!TIP]
> Don't forget to refresh the page.

## Local Development

If you can connect to the dev environment but still have issues such as; `403 - Forbidden Error` on your local, there are few steps you can follow to resolve this:

- Using dev tools on your browser, go to Application tab and clear data for Local Storage, Session Storage and Cookies.

- If the problem persists you may need to temporarily pause your VPN while you work on FFT on your local.

## Running docker-compose run with port access

```
docker-compose run --service-ports
```

## Important notes on design

We use Django Guardian for model instance level permissions https://github.com/django-guardian/django-guardian

Django Guardian **should not be used directly**. There is a set of wrapper functions in _forecast.permission_shortcuts_

These add an additional permission check for the user being able to view forecasts at all.

## Creating data/non-auto migrations

When adding data or non-auto generated migrations, please use the convention:

```
[number]_data_[date]_[time]
```

for example:

```
0004_data_20200501_1345
```

### Running BDD tests

## Run BDD front end from host machine

```bash
npm run bdd
```

## SSH into web container

```bash
docker compose exec web bash
```

## Run BDD tests

```bash
python manage.py behave --settings=config.settings.bdd
```

## Notes

In order to get the node docker container working, this guide was followed: https://jdlm.info/articles/2019/09/06/lessons-building-node-app-docker.html

## Managing user permissions

4 management commands have been added to make dealing with user cost centre easier:

- add_user_to_cost_centre
- cost_centre_users
- remove_user_from_cost_centre
- user_permissions

The names of the management commands denote their function.

## Permissions within the system

### Any logged in SSO user

- Access Chart of Account Gifts and Hospitality Register

### Specific permissions

- Upload budget and Oracle actuals file
- Download Oscar report file
- View forecast (permission to view all forecast data)
- Edit 1 - n cost centres (specific user can edit cost centre data)

### Migrating to new user model (to be removed once complete)

- Take the system off line
- Add username field to HistoricalUser table (max length 150, allow null)
- Amend the custom_usermodel table to be the same as the new User app one
- Add the user app initial migration to the list of django migrations that have been run
- Deploy new codebase
