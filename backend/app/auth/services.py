import json
from databases import Database
from redis.asyncio import Redis
from fastapi.responses import ORJSONResponse
from datetime import datetime, timedelta, timezone

from app.auth.config import auth_settings
from app.auth.utils import generate_token, set_token_cookies


async def generate_token_cookie(
    response: ORJSONResponse, redis: Redis, client_id: str, user_id: str
):
    """
    Generate and store access and refresh tokens for the user, and set them in cookies.

    This function generates both access and refresh tokens for a user, stores the refresh token in the database,
    and sets both tokens in HTTP-only cookies for secure authentication. The access token is used for immediate
    authentication, while the refresh token is used to obtain new access tokens when the current one expires.

    Args:
        db (Connection): The database connection to interact with the refresh tokens table.
        user_id (str): The unique identifier of the user for whom the tokens are generated.
        response (ORJSONResponse): The response object used to set the tokens as cookies.

    """
    # Create access token
    access_token, access_expires_at = await generate_token(
        "access_token",
        auth_settings.ACCESS_SECRET_KEY,
        auth_settings.ALGORITHM,
        auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        client_id,
        user_id,
    )

    # Create refresh token
    refresh_token, refresh_expires_at = await generate_token(
        "refresh_token",
        auth_settings.REFRESH_SECRET_KEY,
        auth_settings.ALGORITHM,
        auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        client_id,
        user_id,
    )

    # Store refresh token
    await save_refresh_token(
        redis, refresh_token, refresh_expires_at, client_id, user_id
    )

    # Set cookies
    set_token_cookies(
        response, access_token, access_expires_at, refresh_token, refresh_expires_at
    )


async def save_refresh_token(
    redis: Redis,
    refresh_token: str,
    expires_in: int | datetime,
    client_id: str,
    user_id: str,
):
    """Save refresh_token"""
    if isinstance(expires_in, datetime):
        expires_in = expires_in - datetime.now(timezone.utc)
    value = json.dumps({"client_id": client_id, "user_id": user_id})
    await redis.setex(refresh_token, expires_in, value)


async def get_refresh_token(redis: Redis, refresh_token: str) -> str | None:
    """Get refresh_token"""
    return await redis.get(refresh_token)


async def delete_refresh_token(redis: Redis, refresh_token: str):
    """Delete refresh_token"""
    await redis.delete(refresh_token)
