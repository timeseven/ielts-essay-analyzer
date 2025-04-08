import json
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock

import pytest

from app.auth.utils import save_refresh_token


@pytest.mark.asyncio
async def test_save_refresh_token_with_timedelta_expiration():
    """
    Tests that `save_refresh_token` saves a refresh token in Redis with its associated
    client_id and user_id when given a timedelta expiration time.

    Verifies that the `setex` method is called with the correct arguments.
    """
    mock_redis = AsyncMock()
    refresh_token = "refresh123"
    expires_in = 3600  # seconds
    client_id = "client_xyz"
    user_id = "user_abc"

    await save_refresh_token(mock_redis, refresh_token, expires_in, client_id, user_id)

    mock_redis.setex.assert_called_once_with(
        refresh_token, expires_in, json.dumps({"client_id": client_id, "user_id": user_id})
    )


@pytest.mark.asyncio
async def test_save_refresh_token_with_datetime_expiration():
    """
    Tests that `save_refresh_token` saves a refresh token in Redis with its associated
    client_id and user_id when given a datetime expiration time.

    Verifies that the `setex` method is called with the correct arguments. The expiration
    time should be between 3598 and 3600 seconds.
    """
    mock_redis = AsyncMock()
    refresh_token = "refresh456"
    expires_in = datetime.now(timezone.utc) + timedelta(hours=1)
    client_id = "client_123"
    user_id = "user_456"

    await save_refresh_token(mock_redis, refresh_token, expires_in, client_id, user_id)

    called_args = mock_redis.setex.call_args[0]
    assert called_args[0] == refresh_token
    assert called_args[2] == json.dumps({"client_id": client_id, "user_id": user_id})

    # The expiration time should be between 3598 and 3600 seconds
    assert 3598 <= called_args[1].total_seconds() <= 3600
