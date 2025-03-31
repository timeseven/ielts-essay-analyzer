import jwt
import uuid
from databases import Database
from redis.asyncio import Redis
from fastapi.responses import ORJSONResponse
from datetime import datetime, timedelta, timezone

from app.auth.config import auth_settings
from app.auth.utils import generate_token, set_token_cookies


async def generate_token_cookie(response: ORJSONResponse, client_id: str, user_id: str):
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

    # Set cookies
    set_token_cookies(
        response, access_token, access_expires_at, refresh_token, refresh_expires_at
    )


async def get_refresh_token(redis: Redis, refresh_token: str) -> dict | None:
    pass
