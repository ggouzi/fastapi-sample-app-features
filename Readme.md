## API (FASTAPI)
- Oauth2 tokens
  hash password
  salt
- Multi platform tokens
- Versioning OK
- Prometheus custom metrics
- Redoc OK
- Static files OK
- Crons OK
- Roles
- Logging OK
- Schema
- Admin password OK

# Todo
Clean code
Write readme
pytest

push image


# FastAPI-app-sample


## Purpose


## Architecture

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



### Database schema
The database schema used in this example is straighforward. Users can create/update/get/delete Items. Each item is assigned to a User (by default, the ones who created it).
Other tables are less relevant from a project perspective.
- Tokens table stores tokens for Users Authentication. See [Authentication](#Authentication)
- Roles tables stores a static list of roles (each role is mapped to an ID). See [Permissions](#Permissions)
- Versions table stores each version in a form of a string and is attached to a boolean flag to specify if the version is supported or not. See [Versioning](#Versioning)

![Database schema](documentation/fastapi-app-db.jpg)

## Features


### Versioning
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

### Authentication
Oauth 2
Routes are protected to be avaialble to logged-in users only.
Authentication works using 2 tokens: An access_token and a refresh_token



### Permissions


## Crons
Cron can be configured using the (BackgroundScheduler module)[Link ???].
They are defined easily using a decorator
```python
# This cron will run at an interval of 1 day (everyday) and will:
# - Open a connection to the database
# - Fetch expired access_token (where access_token_expiration<now) and delete them
# - Close the connection to the database. Closing the connection in the end is important to not leave open conections waiting forever and wasting the pool of connections defined in the database configuration
@sched.scheduled_job('interval', days=1)
def delete_expired_tokens():
    db = SessionLocal()
    db_tokens = token_crud.delete_expired_tokens(db=db)
    logger.info(f"Tokens: Expired tokens deleted: {db_tokens}")
    db.close()
```

You then call `sched.start()` to start the cron

You should observe such logs when you start the app. This means the cron job is currently running
```
2023-10-17 19:40:27,831 [INFO] Added job "delete_expired_tokens" to job store "default"
2023-10-17 19:40:27,831 [INFO] Scheduler started
```

### Serve static files
We can configure the FastAPI app to serve static files using the following command
```python
app.mount("/", StaticFiles(directory="static/files/"))
```

This maps files under `static/files/` folder at the root level of the web server (`/`). `static/files/logo.jpg` could be fetched from `http://localhost:8080/logo.png`


### Logging
This sample app uses logging package as part of standard Python library. The logging configuration is defined in `main.py`
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger()
# Print something
logging.info("A simple message")
logging.warning("A warning message")
logging.error("An error message")
```

```
2023-10-20 11:00:37,526 [INFO] A simple message
2023-10-20 11:00:37,526 [WARNING] A warning message
2023-10-20 11:00:37,526 [ERROR] An error message
```

### Documentation
One of the great features of FastAPI is the [automatic generation of API documentation](https://fastapi.tiangolo.com/tutorial/metadata/). It supports two documentation interfaces: Swagger and Redoc. In this example, we use Redoc.

First of all we need to define the openapi.json endpoint which will then be used to generate the Redoc documentation. We generate the endpoint /openai.json, which will return the OpenAPI schema in a JSON format. This function uses HTTPBasicCredentials and therefore documentation route can be protected with username/password authentication.

```python
# Docs
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    openapi_schema = get_openapi(
        title="Sample API Documentation",
        version="1.0.0",
        routes=app.routes,
        description="Postman Collection: https://api.postman.com/collections/1999344-93e21dc5-aa22-4fbf-a196-fcb5e5f1926c?access_key=PMAT-01HCWNW2JZVWXF79N5ESXY61TT",
        openapi_version="3.0.3",
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "/logo.jpg"
    }
    app.openapi_schema = openapi_schema
    return JSONResponse(openapi_schema)
```

In the following block of code, from main.py, we generate the Redoc documentation from the OpenAPI JSON documentation endpoint we previously configured, /openapi.json. We serve it on /docs route.
```python
@app.get("/docs", include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
  ...
  return get_redoc_html(openapi_url="/openapi.json", title="docs")
```

The documentation can be accessed on [localhost:8080/docs](localhost:8080/docs) and is generated from the signature of the APIRouter fonctions (under /api folder). There is by default a single user in the database sample: username: *admin* / password: *admin*
![Doc](documentation/doc.png)
```python
@router.post("/items", response_model=item_schema.ItemResponse, status_code=201, responses=get_responses([201, 401, 403, 409, 422, 426, 500]), tags=["Items"], description="Create an Item object. Permission=User")
```

### Prometheus
https://github.com/trallnag/prometheus-fastapi-instrumentator



## Postman collection

Postman collection available here: [here](https://api.postman.com/collections/1999344-93e21dc5-aa22-4fbf-a196-fcb5e5f1926c?access_key=PMAT-01HCWNW2JZVWXF79N5ESXY61TT)

## Testing

## Installation

### Local setup standalone
mysql -u root < database/base/01_init_db.sql
mysql -u root < database/base/02_schema.sql
mysql -u root < database/base/03_data.sql

```bash
pip3 install -r app/requirements.txt
```

### Local setup docker-compose
```bash
docker-compose up
```
