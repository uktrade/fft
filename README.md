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
> A database named "fido" will be automatically created.

Open a second terminal and run the following to set up the frontend.

```bash
# install the dependencies
npm install
# start the dev server
npm run dev
```

You should now be able to access the application at http://localhost:8000/.

If you want full admin access, you can elevate your user by running:

```bash
make elevate
```

> [!TIP]
> Don't forget to refresh the page.

## Local Development

If you can connect to the dev environment but still have issues such as `403 - Forbidden Error` on your local, there are a few steps you can follow to resolve this:

- Using dev tools on your browser, go to the Application tab and clear data for Local Storage, Session Storage and Cookies.

- If the problem persists you may need to temporarily pause your VPN while you work on FFT on your local.

## Running docker-compose run with port access

```
docker-compose run --service-ports
```

## Running the BDD tests

Run the chrome container:

```bash
docker compose up -d chrome
```

Build the frontend assets:

```bash
npm run build
```

Run the tests:

```bash
make bdd
```

## Running the Python tests

Run all tests:

```bash
make test
```

Run a single test or file:

```bash
make test test=path/to/test.py::test_name_here
```

## Notes

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

### Managing user permissions

4 management commands have been added to make dealing with user cost centre easier:

- add_user_to_cost_centre
- cost_centre_users
- remove_user_from_cost_centre
- user_permissions

The names of the management commands denote their function.

### Data lake API

Swagger UI docs can be found at `/api/schema/swagger-ui/`.

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

## Setup DebugPy

Add environment variable in your .env file

```bash
ENABLE_DEBUGPY=True
```

Create launch.json file inside .vscode directory

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: Remote Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "0.0.0.0",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "/app/"
        }
      ]
    }
  ]
}
```

## Implementation notes

### Reducers

All the reducers in `front_end/src/Reducers/` are for the `Forecast` React "app".

### ForecastMonthlyFigure

`ForecastMonthlyFigure` is treated as a sparse matrix of actual/forecast data. What do I
mean by this? Well if the `amount` is `0`, then the object is not always created and
therefore does not exist. The code then relies on a default behaviour when the object
related to that figure does not exist.

I guess that this was done to reduce the number of rows that would be needed in that
table.

**Examples**

- Paste to excel - not created if amount is 0
- Edit forecast table cell - created regardless

### Rounding

> For context, FFT stores monetary values as integer pence.

I have found that FFT is using a couple of different rounding methods. The differences
could introduce unexpected behaviour so I wanted to document the differences here.

Python's `round` uses a round to nearest even number approach.

```python
round(0.5) == 0
round(1.5) == 2
```

JavaScript's `Math.round` uses a round half up to nearest number approach.

```javascript
Math.round(0.5) === 1;
Math.round(1.5) === 2;
```

NumPy's `numpy.round` uses a round to nearest even number approach as well.

Python's `Decimal` is also used to parse decimal numbers which are then multiplied by
100 and stored in Django's `IntegerField`. This will truncate the decimal point numbers,
effectively flooring them.

It might be that these inconsistencies don't come up in practice, or that they are there
on purpose and expected/useful to users. However, I still think it's worth noting that
all these approaches are used and that there could be issues.
