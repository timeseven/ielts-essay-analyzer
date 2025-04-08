import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.responses import ORJSONResponse

from app.auth.config import auth_settings
from app.auth.deps import oauth2_scheme


@pytest.mark.asyncio
async def test_auth_deps_with_no_access_token_valid_refresh_token():
    """
    Tests that the `oauth2_scheme` dependency correctly handles a request with a valid refresh token.

    Verifies that when an access token is not provided, the refresh token is used to
    generate a new access token and set it in the response cookies. Ensures that the
    correct calls are made to retrieve the refresh token, generate a new access token,
    and set the token cookies.
    """

    mock_response = MagicMock(spec=ORJSONResponse)
    mock_redis = AsyncMock()

    mock_redis.get.return_value = json.dumps({"client_id": "test_client_id", "user_id": "test_user_id"})

    with (
        patch("app.auth.deps.get_refresh_token") as mock_get_refresh_token,
        patch("app.auth.deps.generate_token") as mock_generate_token,
        patch("app.auth.deps.set_token_cookies") as mock_set_cookies,
    ):
        mock_get_refresh_token.return_value = json.dumps({"client_id": "test_client_id", "user_id": "test_user_id"})

        expiration_time = datetime.now() + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        mock_generate_token.return_value = ("new_access_token", expiration_time)

        result = await oauth2_scheme(
            response=mock_response, redis=mock_redis, access_token=None, refresh_token="valid_refresh_token"
        )

        assert result == {"access_token": "new_access_token"}

        mock_get_refresh_token.assert_called_once_with(mock_redis, "valid_refresh_token")

        mock_generate_token.assert_called_once_with(
            "access_token",
            mock_generate_token.call_args[0][1],  # auth_settings.ACCESS_SECRET_KEY
            mock_generate_token.call_args[0][2],  # auth_settings.ALGORITHM
            mock_generate_token.call_args[0][3],  # auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            "test_client_id",
            "test_user_id",
        )
        mock_set_cookies.assert_called_once_with(mock_response, "new_access_token", expiration_time, None, None)
