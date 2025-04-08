import json
from typing import Annotated, Any, cast

from fastapi import Cookie, Depends
from fastapi.openapi.models import OAuthFlows
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2

from app.auth.config import auth_settings
from app.auth.exceptions import NotAuthenticated
from app.auth.utils import generate_token, get_refresh_token, set_token_cookies
from app.config import settings
from app.db.deps import RedisDep


class CookieJWTAuth(OAuth2):
    def __init__(
        self,
        tokenUrl: str = "",
        scopes: dict[str, str] = {},
    ):
        """
        Initialize the CookieJWTAuth class with token URL and scopes.

        Args:
            tokenUrl (str): The URL to obtain the token from the OAuth2 provider.
            scopes (dict[str, str]): A dictionary of available scopes for OAuth2.
        """
        super().__init__(
            flows=OAuthFlows(password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})),
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
        """
        Verify the access token cookie and return the token value.

        If the access token cookie is not provided, verify the refresh token cookie
        and generate a new access token. Set the new access token in the response
        cookies.

        Args:
            response (ORJSONResponse): The response object used to set cookies.
            redis (RedisDep): The Redis connection used to store and retrieve tokens.
            access_token (Annotated[str | None, Cookie(alias="access_token")]):
                The access token cookie value.
            refresh_token (Annotated[str | None, Cookie(alias="refresh_token")]):
                The refresh token cookie value.

        Returns:
            dict[str, str]: A dictionary containing the access token value.
        """
        # If access token is not provided
        if access_token is None:
            # Get refresh token from redis
            if refresh_token is None:
                raise NotAuthenticated
            else:
                try:
                    refresh_token = await get_refresh_token(redis, refresh_token)
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
                except Exception:
                    raise NotAuthenticated

        return {"access_token": access_token}


oauth2_scheme = CookieJWTAuth(tokenUrl=f"{settings.API_V1_STR}/auth/login")

AccessDep = Annotated[str, Depends(oauth2_scheme)]
