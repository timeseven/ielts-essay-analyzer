import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.config import settings
from app.db.postgresql import postgresql_config
from app.db.redis import redis_config
from app.routes import api_router
from app.utils import error_response

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await postgresql_config.connect()
    except Exception as e:
        logger.error(f"PostgreSQL error during lifespan: {e}")
        raise

    try:
        await redis_config.connect()
    except Exception as e:
        logger.error(f"Redis error during lifespan: {e}")
        raise

    yield

    try:
        await postgresql_config.disconnect()
        await redis_config.disconnect()
    except Exception as e:
        logger.error(f"Database close error during lifespan: {e}")


app = FastAPI(
    default_response_class=ORJSONResponse,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


# Exception handler for FastAPI reqeust validation exceptions
# Note: Must use the pydantic schema inside the route parameters,
# otherwise it will trigger ValidationError from pydantic core
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for error in exc.errors():
        error_msg = error.get("msg")
        if "ctx" in error and "error" in error["ctx"]:
            error_msg = str(error["ctx"]["error"])
        formatted_errors.append({error["loc"][1]: error_msg})
    return error_response(status_code=422, message=formatted_errors)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(status_code=exc.status_code, message=exc.detail)


app.include_router(api_router, prefix=settings.API_V1_STR)
