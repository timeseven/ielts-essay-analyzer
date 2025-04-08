from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from databases import Database
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from app.auth.services import AuthService


@pytest.fixture
def mock_db():
    return AsyncMock(spec=Database)


@pytest.fixture
def mock_redis():
    return AsyncMock(spec=Redis)


@pytest.fixture
def mock_response():
    return MagicMock(spec=ORJSONResponse)


@pytest.fixture
def auth_service(mock_db, mock_redis, mock_response):
    return AuthService(db=mock_db, redis=mock_redis, response=mock_response)


@pytest.mark.asyncio
async def test_login(auth_service):
    """
    Tests the AuthService.login method.

    This test case verifies that the method correctly updates the user's profile last login
    time and generates a token cookie.

    """
    username = "testuser"
    email = "6a0p9@example.com"
    password = "testpassword"

    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_user.username = username
    mock_user.email = email

    mock_profile = MagicMock()

    with patch("app.auth.services.UserService", autospec=True) as MockUserService:
        user_service_instance = MockUserService.return_value
        user_service_instance.update_profile_login = AsyncMock(return_value=mock_profile)
        with patch("app.auth.services.authenticate_user", autospec=True) as mock_authenticate_user:
            mock_authenticate_user.return_value = mock_user
            with patch("app.auth.services.generate_token_cookie", autospec=True) as mock_generate_token_cookie:
                # Call the method under test
                result = await auth_service.login(username, password)

                # Assertions
                mock_authenticate_user.assert_called_once_with(auth_service.db, username, password)
                user_service_instance.update_profile_login.assert_called_once_with(
                    mock_user.current_client_id, mock_user.id
                )
                mock_generate_token_cookie.assert_called_once_with(
                    auth_service.response, auth_service.redis, str(mock_user.current_client_id), str(mock_user.id)
                )

                assert result == mock_profile
