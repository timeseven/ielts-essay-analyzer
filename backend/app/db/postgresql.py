from databases import Database, DatabaseURL

from app.db.config import db_settings


class PostgresqlConfig:
    def __init__(
        self,
        url: DatabaseURL | str,
        min_size: int,
        max_size: int,
        timeout: float,
        max_inactive_connection_lifetime: float,
    ):
        """
        Initialize a PostgresqlConfig instance.

        Args:
            url (DatabaseURL | str): The URL of the PostgreSQL database.
            min_size (int): The minimum number of connections to keep open in the connection pool.
            max_size (int): The maximum number of connections to keep open in the connection pool.
            timeout (float): The timeout in seconds for acquiring a connection from the pool.
            max_inactive_connection_lifetime (float): The maximum lifetime of an inactive connection
            in the connection pool.
        """
        self.db_pool = Database(
            url,
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
        )

    async def connect(self):
        """
        Connect to the PostgreSQL database asynchronously.

        This function is a coroutine that connects to the PostgreSQL
        database asynchronously. It is a part of the Database class
        and is used to create a connection pool to the database.

        Returns:
            None
        """
        await self.db_pool.connect()

    async def disconnect(self):
        """
        Disconnect from the PostgreSQL database asynchronously.

        This function is a coroutine that disconnects from the PostgreSQL
        database asynchronously. It is a part of the Database class
        and is used to close all connections in the connection pool to the database.

        Returns:
            None
        """
        await self.db_pool.disconnect()


postgresql_config = PostgresqlConfig(
    url=db_settings.ASYNC_DATABASE_URL,
    min_size=db_settings.DATABASE_MIN_CONNECTIONS,
    max_size=db_settings.DATABASE_MAX_CONNECTIONS,
    timeout=db_settings.DATABASE_TIMEOUT,
    max_inactive_connection_lifetime=db_settings.DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME,
)
