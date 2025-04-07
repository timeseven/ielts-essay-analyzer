import jwt
import json
import bcrypt
from redis.asyncio import Redis
from fastapi.responses import ORJSONResponse
from datetime import datetime, timedelta, timezone

# Config
from app.auth.config import auth_settings


# Verify if the plain password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# Hash the provided password
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


# Generate an  token for the given user_id
async def generate_token(
    token_type: str,
    secret_key: str,
    algorithm: str,
    expires_minutes: int,
    client_id: str,
    user_id: str,
) -> dict:
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


# Set the access token and refresh token cookies
def set_token_cookies(
    response: ORJSONResponse,
    access_token: str,
    access_expires_at: datetime,
    refresh_token: str,
    refresh_expires_at: datetime,
):
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
