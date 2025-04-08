from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.responses import ORJSONResponse

from app.auth.deps import oauth2_scheme


@pytest.mark.asyncio
async def test_auth_deps_with_valid_access_token():
    """
    Tests that the `oauth2_scheme` dependency correctly handles a request with a valid access token.

    Verifies that the dependency returns a dictionary with the access token key set to the value of the access token,
    and that a call to `get` is not made on the Redis mock.
    """
    mock_response = MagicMock(spec=ORJSONResponse)
    mock_redis = AsyncMock()

    result = await oauth2_scheme(
        response=mock_response, redis=mock_redis, access_token="valid_access_token", refresh_token="valid_refresh_token"
    )
    assert result == {"access_token": "valid_access_token"}
    mock_redis.get.assert_not_called()
