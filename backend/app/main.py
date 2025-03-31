import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.routes import api_router

from app.config import settings

from app.db.redis import redis_config
from app.db.postgresql import postgresql_config


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


app.include_router(api_router, prefix=settings.API_V1_STR)
