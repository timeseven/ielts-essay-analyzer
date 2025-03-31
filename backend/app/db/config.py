from app.config import BaseSettings
from databases import DatabaseURL


class DbConfig(BaseSettings):
    # PostgreSQL settings
    DATABASE_URL: DatabaseURL | str
    ASYNC_DATABASE_URL: DatabaseURL | str
    DATABASE_MIN_CONNECTIONS: int = 10
    DATABASE_MAX_CONNECTIONS: int = 20
    DATABASE_TIMEOUT: int = 30
    DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME: int = 180

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int


db_settings = DbConfig()
