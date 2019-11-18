# fido

## The Project



## Set up

A database called "fido" will be automatically created.

Run the following to perform initial migrations:

```
docker-compose run fido python manage.py migrate
```

In order to add stub data for local development purposes run:

```
docker-compose run fido python manage.py create_stub_data All
```

You can add forecast data if you are developing forecast related functions:

```
docker-compose run fido python manage.py create_stub_forecast_data
```

Now access any page within the site and log in with your single sign on credentials.

You now need to elevate your user permissions in order to access the admin tool. You can do this by running:

```
docker-compose run fido python manage.py elevate_sso_user_permissions
```

### Environment variables

You need to populate the .env file in the project root folder with the following variables:

* AUTHBROKER_CLIENT_ID
* AUTHBROKER_CLIENT_SECRET

These can be provided by a member of the team.

### Integration between Django and React

The process described in this post was followed: 
https://www.techiediaries.com/django-react-rest/

### Running docker-compose run with port access
```
docker-compose run --service-ports
```

### Important notes on design

We use Django Guardian for model instance level permissions https://github.com/django-guardian/django-guardian

Django Guardian **should not be used directly**. There is a set of wrapper functions in *forecast.permission_shortcuts*

These add an additional permission check for the user being able to view forecasts at all.


## TODO
Try increasing size of container machine and see if npm start will work
Add setup steps to make file and amend readme

### Questions

Have we used any indexes in the database?



### Notes
In order to get the node docker container working, this guide was followed: https://jdlm.info/articles/2019/09/06/lessons-building-node-app-docker.html

### Product URLs

#### Dev URL
https://fido.trade.uat.uktrade.io/core/

#### Production URL
https://fido.trade.gov.uk/core/

### Managing user permissions

4 management commands have been added to make dealing with user cost centre easier:

 * add_user_to_cost_centre
 * cost_centre_users
 * remove_user_from_cost_centre
 * user_permissions
 
The names of the management commands denote their function.
