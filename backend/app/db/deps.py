from typing import Annotated, AsyncGenerator

from databases import Database
from fastapi import Depends
from redis.asyncio import Redis

from app.db.postgresql import postgresql_config
from app.db.redis import redis_config


async def write_db_transaction() -> AsyncGenerator[Database, None]:
    """
    Acquire a transaction for write operations as db dependency.

    This function is a fastapi dependency that yields a transaction
    for write operations. This transaction is configured with
    isolation level 'read committed', readonly=False, and deferrable=False.

    Yields:
        Database: a database instance with a transaction
    """
    async with postgresql_config.db_pool.transaction(isolation="read_committed", readonly=False, deferrable=False):
        yield postgresql_config.db_pool


async def read_db_transaction() -> AsyncGenerator[Database, None]:
    """
    Acquire a transaction for read operations as db dependency.

    This function is a FastAPI dependency that yields a transaction
    for read operations. This transaction is configured with
    isolation level 'repeatable read', readonly=True, and deferrable=True.

    Yields:
        Database: a database instance with a transaction
    """

    async with postgresql_config.db_pool.transaction(isolation="repeatable_read", readonly=True, deferrable=True):
        yield postgresql_config.db_pool


async def get_db() -> AsyncGenerator[Database, None]:
    """
    Acquire the databases pool as db dependency.

    This function is a FastAPI dependency that yields the databases pool
    for single query operations.

    Yields:
        Database: a database instance
    """
    yield postgresql_config.db_pool


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Acquire the Redis client as a dependency.

    This function is a FastAPI dependency that yields the Redis client
    for performing Redis operations.

    Yields:
        Redis: a Redis client instance
    """

    yield redis_config.redis_client


WriteDbDep = Annotated[Database, Depends(write_db_transaction)]
ReadDbDep = Annotated[Database, Depends(read_db_transaction)]
SimpleDbDep = Annotated[Database, Depends(get_db)]
RedisDep = Annotated[Redis, Depends(get_redis)]
