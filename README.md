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

## TODO
Try increasing size of container machine and see if npm start will work

### Questions

Have we used any indexes in the database?
aaaaa
