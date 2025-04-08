from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.responses import ORJSONResponse

from app.auth.deps import oauth2_scheme
from app.auth.exceptions import NotAuthenticated


@pytest.mark.asyncio
async def test_auth_deps_with_no_access_token_invalid_refresh_token():
    """
    Tests that the `oauth2_scheme` dependency raises a `NotAuthenticated` exception
    when an access token is not provided and the refresh token is invalid.

    Verifies that the dependency does not make a call to `get` on the Redis mock.
    """
    mock_response = MagicMock(spec=ORJSONResponse)
    mock_redis = AsyncMock()

    mock_redis.get.return_value = None

    with pytest.raises(NotAuthenticated):
        await oauth2_scheme(response=mock_response, redis=mock_redis, access_token=None, refresh_token="invalid_token")

    mock_redis.get.assert_called_once_with("invalid_token")
    mock_response.set_cookie.assert_not_called()
