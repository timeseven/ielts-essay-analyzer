from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.responses import ORJSONResponse

from app.auth.deps import oauth2_scheme
from app.auth.exceptions import NotAuthenticated


@pytest.mark.asyncio
async def test_auth_deps_without_tokens():
    """
    Tests that the `oauth2_scheme` dependency raises a `NotAuthenticated` exception
    when no access or refresh tokens are provided.

    Verifies that the dependency does not make a call to `get` on the Redis mock.
    """
    mock_response = MagicMock(spec=ORJSONResponse)
    mock_redis = AsyncMock()

    with pytest.raises(NotAuthenticated):
        await oauth2_scheme(response=mock_response, redis=mock_redis, access_token=None, refresh_token=None)

    mock_redis.get.assert_not_called()
