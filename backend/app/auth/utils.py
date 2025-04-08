import json
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from app.auth.config import auth_settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain text password matches a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """
    Get the hashed password of a plain text password.

    Uses bcrypt to hash the password. The salt is randomly generated
    for each call to this function.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


async def generate_token(
    token_type: str,
    secret_key: str,
    algorithm: str,
    expires_minutes: int,
    client_id: str,
    user_id: str,
) -> dict:
    """
    Generate an authentication token for a given user_id and client_id.

    Args:
        token_type (str): The type of token to generate. e.g. "access_token" or "refresh_token".
        secret_key (str): The secret key used to sign the token.
        algorithm (str): The algorithm used to sign the token.
        expires_minutes (int): The number of minutes until the token expires.
        client_id (str): The client_id to store in the token.
        user_id (str): The user_id to store in the token.

    Returns:
        dict: A dictionary containing the generated token and its expiration datetime.
    """
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(minutes=expires_minutes)

    token_payload = {
        "client_id": client_id,
        "user_id": user_id,
        "iat": created_at,
        "exp": expires_at,
        "type": token_type,
    }

    token = jwt.encode(
        payload=token_payload,
        key=secret_key,
        algorithm=algorithm,
    )

    return token, expires_at


def set_token_cookies(
    response: ORJSONResponse,
    access_token: str,
    access_expires_at: datetime,
    refresh_token: str,
    refresh_expires_at: datetime,
):
    """
    Set authentication tokens as HTTP-only cookies in the response.

    Args:
        response (ORJSONResponse): The response object used to set cookies.
        access_token (str): The access token value to be set in the cookie.
        access_expires_at (datetime): The expiration datetime for the access token.
        refresh_token (str): The refresh token value to be set in the cookie.
        refresh_expires_at (datetime): The expiration datetime for the refresh token.

    This function sets the access and refresh tokens in the response as
    HTTP-only cookies with secure and samesite attributes. The cookies
    are set to expire at their respective expiration times.
    """
    if access_token and access_expires_at:
        response.set_cookie(
            key="access_token",
            value=access_token,
            path="/",
            domain=None,
            httponly=True,
            secure=True,
            samesite="lax",
            expires=access_expires_at,
        )

    if refresh_token and refresh_expires_at:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            path="/",
            domain=None,
            httponly=True,
            secure=True,
            samesite="lax",
            expires=refresh_expires_at,
        )


async def save_refresh_token(
    redis: Redis,
    refresh_token: str,
    expires_in: int | datetime,
    client_id: str,
    user_id: str,
):
    """
    Store a refresh token in redis with its associated client_id and user_id.

    Args:
        redis (Redis): The Redis database connection.
        refresh_token (str): The refresh token to be stored.
        expires_in (int | datetime): The expiration time (in seconds or as a datetime object)
            for the refresh token.
        client_id (str): The client_id associated with the refresh token.
        user_id (str): The user_id associated with the refresh token.

    This function stores a refresh token in redis with its associated client_id and user_id.
    The refresh token is set to expire after the given time.
    """
    if isinstance(expires_in, datetime):
        expires_in = expires_in - datetime.now(timezone.utc)
    value = json.dumps({"client_id": client_id, "user_id": user_id})
    await redis.setex(refresh_token, expires_in, value)


async def get_refresh_token(redis: Redis, refresh_token: str) -> str | None:
    """
    Retrieve a refresh token from Redis.

    Args:
        redis (Redis): The Redis database connection.
        refresh_token (str): The refresh token to be retrieved.

    Returns:
        str | None: The refresh token value if found, None otherwise.
    """
    return await redis.get(refresh_token)


async def delete_refresh_token(redis: Redis, refresh_token: str):
    """
    Delete a refresh token from Redis.

    Args:
        redis (Redis): The Redis database connection.
        refresh_token (str): The refresh token to be deleted.

    This function deletes a refresh token from redis.
    """
    await redis.delete(refresh_token)


async def generate_token_cookie(response: ORJSONResponse, redis: Redis, client_id: str, user_id: str):
    """
    Generate authentication tokens, store the refresh token in Redis and set tokens in cookies.

    Args:
        response (ORJSONResponse): The response object used to set cookies.
        redis (Redis): The Redis database connection.
        client_id (str): The client_id to store in the token.
        user_id (str): The user_id to store in the token.

    This function generates an access token and a refresh token, stores the refresh token in redis,
    and sets the tokens in the response object as HTTP-only cookies.
    """
    # Generate access token
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
    await save_refresh_token(redis, refresh_token, refresh_expires_at, client_id, user_id)

    # Set cookies
    set_token_cookies(response, access_token, access_expires_at, refresh_token, refresh_expires_at)
