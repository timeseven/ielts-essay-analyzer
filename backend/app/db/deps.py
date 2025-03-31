from databases import Database
from fastapi import Depends
from typing import Annotated, AsyncGenerator
from redis.asyncio import Redis

from app.db.postgresql import postgresql_config
from app.db.redis import redis_config


# Acquire a transaction for write operations as db dependency
async def write_db_transaction() -> AsyncGenerator[Database, None]:
    async with postgresql_config.db_pool.transaction(
        isolation="read_committed", readonly=False, deferrable=False
    ):
        yield postgresql_config.db_pool


# Acquire a read-only transaction for multiple queries as db dependency
async def read_db_transaction() -> AsyncGenerator[Database, None]:
    async with postgresql_config.db_pool.transaction(
        isolation="repeatable_read", readonly=True, deferrable=True
    ):
        yield postgresql_config.db_pool


# Directly yield the databases pool for single query as db dependency
async def get_db() -> AsyncGenerator[Database, None]:
    yield postgresql_config.db_pool


# Redis dependencies
async def get_redis() -> AsyncGenerator[Redis, None]:
    yield redis_config.redis_client


WriteDbDep = Annotated[Database, Depends(write_db_transaction)]
ReadDbDep = Annotated[Database, Depends(read_db_transaction)]
SimpleDbDep = Annotated[Database, Depends(get_db)]
RedisDep = Annotated[Redis, Depends(get_redis)]
