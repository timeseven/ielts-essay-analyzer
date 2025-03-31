import jwt
import bcrypt
from fastapi.responses import ORJSONResponse
from datetime import datetime, timedelta, timezone

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
