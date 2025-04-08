from redis.asyncio import Redis

from app.db.config import db_settings


class RedisConfig:
    def __init__(self, host: str, port: int, decode_responses: bool):
        """
        Initialize a RedisConfig object.

        Args/Attributes:
            host (str): The hostname or IP address to connect to Redis on.
            port (int): The port number to connect to Redis on.
            decode_responses (bool): If set to True, all responses from Redis will be
                decoded to strings with the utf-8 encoding.
            redis_client (Redis): The Redis client object. This is initially set to None,
                and is set to the Redis client object when the connect() method is
                called.
        """
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self.redis_client = None

    async def connect(self):
        """
        Connect to Redis asynchronously.

        This method sets the Redis client object to a connected Redis client.
        The Redis client is set up with the host, port, and decode_responses
        values specified in the RedisConfig object.

        Returns:
            None
        """
        self.redis_client = Redis(
            host=self.host,
            port=self.port,
            decode_responses=self.decode_responses,
        )
        print("Connected to Redis")

    async def disconnect(self):
        """
        Disconnect from Redis asynchronously.

        This method disconnects from Redis if the Redis client object is not None.
        If the Redis client object is not None, it is closed and set to None.

        Returns:
            None
        """
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None


redis_config = RedisConfig(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    decode_responses=True,
)
