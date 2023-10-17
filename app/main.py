import uvicorn
import time
import settings
import logging
import traceback

# FastAPI imports
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse

# SQLAlchemy imports
from sqlalchemy.orm import Session

# Prometheus client import
from prometheus_client import start_http_server
from prometheus_fastapi_instrumentator import Instrumentator

# Project imports
from starlette.responses import JSONResponse
from db.database import get_db
from api import (
    auth_routes,
    item_routes,
    role_routes,
    user_routes,
    version_routes
)
from crud import user_crud
from cron import token_cron
from exceptions.VersionException import VersionException
from exceptions.CustomException import CustomException
from utils import consts

# Imports needed to protect API documentation endpoints
from fastapi.openapi.docs import get_redoc_html

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger()

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Dependencies
app.include_router(auth_routes.router)
app.include_router(item_routes.router)
app.include_router(role_routes.router)
app.include_router(user_routes.router)
app.include_router(version_routes.router)


# HTTP Handlers
@app.exception_handler(CustomException)
async def exception_handler(request: Request, exception: CustomException):
    ex = HTTPException(
        status_code=exception.status_code,
        detail=exception.detail
    )
    logging.error(exception.info)
    return await http_exception_handler(request, ex)


@app.exception_handler(VersionException)
async def version_exception_handler(request: Request, exception: VersionException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": exception.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errs = exc.errors()
    detail = 'Cannot parse request'
    if len(errs) > 0:
        logger.error(errs)
        detail = str(errs[0]['msg'])
    ex = HTTPException(
        status_code=422,
        detail=detail
    )
    return await http_exception_handler(request, ex)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        if request.url.path != '/':
            process_time_seconds = (time.time() - start_time)
            process_time_milli = process_time_seconds * 1000
            request_time_milli = round(process_time_milli, 2)
            request_time_sec = round(process_time_seconds, 2)
            user_agent = request.headers.get("user-agent", "-")
            response_size = response.headers.get("content-length", "-")
            version = response.headers.get("x-version", "-")
            accesslog = f"[zz999] {response.status_code} {request_time_sec} {request_time_milli} {response_size} {request.method} {request.url.path}?{str(request.query_params)} {version} {user_agent}"
            logger.info(accesslog)
        return response
    except Exception as e:
        logger.error("Can't log request")
        logger.error(str(e))
        logger.error(traceback.format_exc())

security = HTTPBasic()


# Docs
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    db_user = user_crud.check_authentication(db, username=credentials.username, password=credentials.password)
    if not db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.INVALID_CREDENTIALS,
            info=f'Cannot find activated User with username {credentials.username} and specified password'
        )

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


@app.get("/docs", include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    db_user = user_crud.check_authentication(db, username=credentials.username, password=credentials.password)
    if not db_user:
        raise CustomException(
            db=db,
            status_code=consts.Consts.ERROR_CODE_401,
            detail=consts.Consts.INVALID_CREDENTIALS,
            info=f'Cannot find activated User with username {credentials.username} and specified password'
        )

    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/", include_in_schema=False)
async def redirect():
    response = RedirectResponse(url='/docs')
    return response

# Crons
token_cron.sched.start()

# Start up the server to expose the metrics.
instrumentator = Instrumentator().instrument(app)
start_http_server(8000)

# Mount static images folder
app.mount("/", StaticFiles(directory="static/files/"))

if __name__ == "__main__":
    instrumentator.expose(app)
    uvicorn.run(app, host='0.0.0.0', port=settings.env.APP_PORT)
