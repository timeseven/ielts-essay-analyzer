from redis.asyncio import Redis

from app.db.config import db_settings


class RedisConfig:
    def __init__(self, host: str, port: int, decode_responses: bool):
        self._host = host
        self._port = port
        self._decode_responses = decode_responses
        self.redis_client = None

    async def connect(self):
        """Connect to Redis"""
        self.redis_client = Redis(
            host=self._host,
            port=self._port,
            decode_responses=self._decode_responses,
        )

    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None


redis_config = RedisConfig(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    decode_responses=True,
)
