import json
from unittest.mock import AsyncMock

import pytest

from app.auth.utils import get_refresh_token


@pytest.mark.asyncio
async def test_get_refresh_token_found():
    """
    Tests that `get_refresh_token` returns the expected value when a refresh token is found
    in Redis.

    Verifies that the function calls Redis' `get` method correctly and that the returned
    value matches the expected value.
    """
    mock_redis = AsyncMock()
    refresh_token = "refresh123"
    expected_value = json.dumps({"client_id": "client_xyz", "user_id": "user_abc"})

    # Mock Redis to return the expected value
    mock_redis.get.return_value = expected_value

    # Call the function
    result = await get_refresh_token(mock_redis, refresh_token)

    # Assert the result matches the expected value
    assert result == expected_value

    # Verify that Redis' get method was called correctly
    mock_redis.get.assert_called_once_with(refresh_token)


@pytest.mark.asyncio
async def test_get_refresh_token_not_found():
    """
    Tests that `get_refresh_token` returns None when a refresh token is not found
    in Redis.

    Verifies that the function calls Redis' `get` method correctly and that the
    returned value is None when the token is not found.
    """
    mock_redis = AsyncMock()
    refresh_token = "refresh_not_found"

    # Mock Redis to return None (token not found)
    mock_redis.get.return_value = None

    # Call the function
    result = await get_refresh_token(mock_redis, refresh_token)

    # Assert the result is None (token not found)
    assert result is None

    # Verify that Redis' get method was called correctly
    mock_redis.get.assert_called_once_with(refresh_token)
