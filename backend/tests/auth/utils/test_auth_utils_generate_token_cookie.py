from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import jwt
import pytest
from fastapi.responses import ORJSONResponse

from app.auth.config import auth_settings
from app.auth.utils import generate_token_cookie


@pytest.mark.asyncio
async def test_generate_token_cookie():
    """
    Test that generate_token_cookie:
    - Generates valid access and refresh tokens
    - Stores the refresh token in Redis with correct structure and expiry
    - Sets both tokens in the response as secure HTTP-only cookies
    """

    # Mock Redis client to prevent actual database usage
    mock_redis = AsyncMock()

    # Create a mock ORJSONResponse object to inspect cookie settings
    mock_response = MagicMock(spec=ORJSONResponse)

    # Define token payload input values
    client_id = "client_id_123"
    user_id = "user_id_456"

    # Call the function under test
    await generate_token_cookie(mock_response, mock_redis, client_id, user_id)

    # Extract cookies from set_cookie call arguments
    cookie_calls = {call.kwargs["key"]: call.kwargs for call in mock_response.set_cookie.mock_calls}

    # Ensure both tokens were set as cookies
    assert "access_token" in cookie_calls
    assert "refresh_token" in cookie_calls

    access_token = cookie_calls["access_token"]["value"]
    refresh_token = cookie_calls["refresh_token"]["value"]

    # Decode JWTs to verify their payloads
    access_payload = jwt.decode(access_token, auth_settings.ACCESS_SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
    refresh_payload = jwt.decode(refresh_token, auth_settings.REFRESH_SECRET_KEY, algorithms=[auth_settings.ALGORITHM])

    # Validate access token payload
    assert access_payload["type"] == "access_token"
    assert access_payload["client_id"] == client_id
    assert access_payload["user_id"] == user_id

    # Validate refresh token payload
    assert refresh_payload["type"] == "refresh_token"
    assert refresh_payload["client_id"] == client_id
    assert refresh_payload["user_id"] == user_id

    # Validate cookie properties for access token
    assert cookie_calls["access_token"]["httponly"] is True
    assert cookie_calls["access_token"]["secure"] is True
    assert cookie_calls["access_token"]["samesite"] == "lax"
    access_expires_at = datetime.fromtimestamp(access_payload["exp"], tz=timezone.utc).replace(microsecond=0)
    cookie_expires_at = cookie_calls["access_token"]["expires"].replace(microsecond=0)
    assert access_expires_at == cookie_expires_at

    # Validate cookie properties for refresh token
    assert cookie_calls["refresh_token"]["httponly"] is True
    assert cookie_calls["refresh_token"]["secure"] is True
    assert cookie_calls["refresh_token"]["samesite"] == "lax"
    refresh_expires_at = datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc).replace(microsecond=0)
    cookie_expires_at = cookie_calls["refresh_token"]["expires"].replace(microsecond=0)
    assert refresh_expires_at == cookie_expires_at

    # Verify that the refresh token was saved to Redis correctly
    mock_redis.setex.assert_awaited()
    redis_key = mock_redis.setex.call_args.args[0]
    redis_expiry = mock_redis.setex.call_args.args[1]
    redis_value = mock_redis.setex.call_args.args[2]

    assert isinstance(redis_key, str)
    assert isinstance(redis_expiry, timedelta)
    assert client_id in redis_value
    assert user_id in redis_value
