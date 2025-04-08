from unittest.mock import AsyncMock

import pytest

from app.auth.utils import delete_refresh_token  # Your actual import path


@pytest.mark.asyncio
async def test_delete_refresh_token():
    """
    Tests that `delete_refresh_token` correctly deletes a refresh token from Redis.

    Verifies that the function calls Redis' `delete` method with the correct refresh token.
    """
    mock_redis = AsyncMock()
    refresh_token = "refresh_to_delete"

    # Call the function to delete the refresh token
    await delete_refresh_token(mock_redis, refresh_token)

    # Verify that the Redis delete method was called with the correct refresh token
    mock_redis.delete.assert_called_once_with(refresh_token)
