## API (FASTAPI)
- Oauth2 tokens
  hash password
  salt
- Multi platform tokens
- Versioning OK
- Prometheus custom metrics
- Redoc
- Static files OK
- Crons
- Roles
- Logging
- Schema
- Admin password

# Todo
Clean code
Write readme
pytest

push image


# Purpose


# Architecture

```
├── app
    ├── api => Controller: Where HTTP routes are defined for each resource and errors handled. Calls either its associated resource crud file or a different resource repository
    ├── cron => Where background tasks are defined
    ├── crud => CRUD operations for each resource. No error handling, all errors handled in api/controller
    ├── db => Manage database connection
    ├── exceptions => Custom exceptions
    ├── models => Serialize resource from database schema into classes
    ├── repository => Middleware used to communicate from api/controller to other cruds
    ├── schemas => Maps intput/output HTTP payload
    ├── static => Serve static files
    ├── test => For testing
    ├── utils => Utilies/common. Functions and constants used multiple times in previous folders
    ├── .env => Define environment variables
    ├── main.py => Import all routes, define cron jobs, generate auto-documentation, start the app
    ├── settings.py => Maps environment variables from .env file to class attributes
    ├── requirements.txt => List all dependencies
```



## Database schema
<Fastapi-app-db.jpg>

# Features


## Versioning
A versioning mechanism is in place by defining a X-Version HTTP header and handle it through a wrapper function on routes using a decorator `@custom_declarators.version_check`
This function checks for the presence of X-Version HTTP header.
- If the header is present, extract its value and compare it with the content of the versions table. Each version is either supported or not
  - If version.supported=True => Allow to continue executing the given route
  - If version.supported=False => Raise a HTTP 426 error
- If the header is absent, allow to continue executing the given route. We consider the absence of header to be fine and similar to a supported version

```bash
# A non-supported version
➭ VERSION=0.9; curl -sSw "\nstatus_code: "%{http_code} http://localhost:8080/roles -H "X-Version: ${VERSION}"
{"detail":"Version not supported anymore"}
status_code: 426
```

```bash
# A supported version        
➭ VERSION=1.0; curl -sSw "\nstatus_code: "%{http_code} http://localhost:8080/roles -H "X-Version: ${VERSION}"
[{"name":"admin","id":1},{"name":"user","id":2}]
status_code: 200
```

## Authentication OAuth2

Routes are protected to be avaialble to logged-in users only.
Authentication works using 2 tokens: An access_token and a refresh_token



# Permissions


## Serve static files
We can configure the FastAPI app to serve static files using the following command
```python
app.mount("/", StaticFiles(directory="static/files/"))
```

This maps files under `static/files/` folder at the root level of the web server (`/`). `static/files/logo.jpg` could be fetched from `http://localhost:8080/logo.png`



## Prometheus
https://github.com/trallnag/prometheus-fastapi-instrumentator



# Postman collection

Postman collection available here: [here](https://api.postman.com/collections/1999344-93e21dc5-aa22-4fbf-a196-fcb5e5f1926c?access_key=PMAT-01HCWNW2JZVWXF79N5ESXY61TT)

# Testing

# Local setup standalone
mysql -u root < database/base/01_init_db.sql
mysql -u root < database/base/02_schema.sql
mysql -u root < database/base/03_data.sql

```bash
pip3 install -r app/requirements.txt
```



# Local setup docker-compose
```bash
docker-compose up
```
