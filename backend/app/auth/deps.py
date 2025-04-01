import json
from typing import Annotated, Any, cast
from fastapi import Cookie, Depends
from fastapi.openapi.models import OAuthFlows
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2

from app.config import settings

# Auth
from app.auth.config import auth_settings
from app.auth.services import (
    get_refresh_token,
    set_token_cookies,
)
from app.auth.utils import generate_token
from app.auth.exceptions import NotAuthenticated

from app.db.deps import RedisDep


class CookieJWTAuth(OAuth2):
    """
    Custom JWT Cookie Authentication for FastAPI.

    This authentication class extends FastAPI's OAuth2 to implement JWT-based authentication via cookies.
    Unlike traditional header-based authentication, this method stores and retrieves JWTs from HTTP-only cookies,
    enhancing security by reducing exposure to frontend scripts.

    Key Features:
    - Access Token Management: Retrieves access tokens from cookies and validates them.
    - Automatic Renewal: If the access token is missing, it attempts to renew and update access token in cookies
      using a valid refresh token.
    - OAuth2 Compatibility: Inherits from OAuth2, making it compatible with FastAPI security schemes.

    Attributes:
        tokenUrl (str): The URL endpoint for token retrieval.
        scopes (dict): Dictionary defining OAuth2 scopes for authorization.

    """

    def __init__(
        self,
        tokenUrl: str = "",
        scopes: dict[str, str] = {},
    ):
        super().__init__(
            flows=OAuthFlows(
                password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
            ),
            scheme_name="Cookie",
            auto_error=True,
        )

    async def __call__(
        self,
        response: ORJSONResponse,
        redis: RedisDep,
        access_token: Annotated[
            str | None,
            Cookie(alias="access_token"),
        ] = None,
        refresh_token: Annotated[
            str | None,
            Cookie(alias="refresh_token"),
        ] = None,
    ):
        # If access token is not provided
        if access_token is None:
            # Get refresh token from redis
            refresh_token = await get_refresh_token(redis, refresh_token)
            if refresh_token is None:
                raise NotAuthenticated
            else:
                refresh_token = json.loads(refresh_token)
                # Generate new access token
                client_id = str(refresh_token.get("client_id"))
                user_id = str(refresh_token.get("user_id"))
                access_token, access_expires_at = await generate_token(
                    "access_token",
                    auth_settings.ACCESS_SECRET_KEY,
                    auth_settings.ALGORITHM,
                    auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                    client_id,
                    user_id,
                )
                set_token_cookies(
                    response,
                    access_token,
                    access_expires_at,
                    None,
                    None,
                )

        return {"access_token": access_token}


oauth2_scheme = CookieJWTAuth(tokenUrl=f"{settings.API_V1_STR}/auth/login")

AccessDep = Annotated[str, Depends(oauth2_scheme)]
