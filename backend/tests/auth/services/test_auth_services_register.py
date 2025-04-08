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
async def test_register_with_new_user_and_client(auth_service):
    """
    Tests the AuthService.register method when registering a new user and client.

    This test case provides a new client name and no client ID, and verifies that
    the UserService.create_user, ClientService.create_client, UserService.update_user_current_client,
    UserService.create_profile, and generate_token_cookie methods are called with the expected
    arguments.
    """
    username = "testuser"
    email = "6a0p9@example.com"
    password = "testpassword"
    client_name = "Test Client"
    client_id = None

    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_user.username = username
    mock_user.email = email

    mock_client = MagicMock()
    mock_client.id = uuid4()
    mock_client.name = client_name

    mock_profile = MagicMock()

    with patch("app.auth.services.UserService", autospec=True) as MockUserService:
        user_service_instance = MockUserService.return_value
        user_service_instance.create_user = AsyncMock(return_value=mock_user)
        user_service_instance.update_user_current_client = AsyncMock()
        user_service_instance.create_profile = AsyncMock(return_value=mock_profile)

        with patch("app.auth.services.ClientService", autospec=True) as MockClientService:
            client_service_instance = MockClientService.return_value
            client_service_instance.create_client = AsyncMock(return_value=mock_client)

            with patch("app.auth.services.generate_token_cookie", autospec=True) as mock_generate_token_cookie:
                # Call the method under test
                result = await auth_service.register(
                    username=username, email=email, password=password, client_name=client_name, client_id=client_id
                )

                # Assertions
                MockUserService.assert_called_once_with(auth_service.db)
                client_service_instance.create_client.assert_called_once_with(name=client_name)

                user_service_instance.update_user_current_client.assert_called_once_with(mock_user.id, mock_client.id)

                user_service_instance.create_profile.assert_called_once_with(
                    client_id=mock_client.id, user_id=mock_user.id, full_name=mock_user.username, is_client_owner=True
                )

                mock_generate_token_cookie.assert_called_once_with(
                    auth_service.response, auth_service.redis, str(mock_client.id), str(mock_user.id)
                )

                assert result == mock_profile


@pytest.mark.asyncio
async def test_register_with_new_user_and_existing_client(auth_service):
    """
    Tests the AuthService.register method when registering a new user with an existing client.

    This test case provides an existing client ID and no client name, and verifies that
    the UserService.create_user, UserService.update_user_current_client, UserService.create_profile,
    and generate_token_cookie methods are called with the expected arguments.
    """
    username = "testuser"
    email = "6a0p9@example.com"
    password = "testpassword"
    client_name = None
    client_id = uuid4()

    mock_user = MagicMock()
    mock_user.id = uuid4()
    mock_user.username = username
    mock_user.email = email

    mock_profile = MagicMock()

    with patch("app.auth.services.UserService", autospec=True) as MockUserService:
        user_service_instance = MockUserService.return_value
        user_service_instance.create_user = AsyncMock(return_value=mock_user)
        user_service_instance.update_user_current_client = AsyncMock()
        user_service_instance.create_profile = AsyncMock(return_value=mock_profile)

        with patch("app.auth.services.generate_token_cookie", autospec=True) as mock_generate_token_cookie:
            # Call the method under test
            result = await auth_service.register(
                username=username, email=email, password=password, client_name=client_name, client_id=client_id
            )

            # Assertions
            MockUserService.assert_called_once_with(auth_service.db)

            user_service_instance.update_user_current_client.assert_called_once_with(mock_user.id, client_id)

            user_service_instance.create_profile.assert_called_once_with(
                client_id=client_id, user_id=mock_user.id, full_name=mock_user.username, is_client_owner=True
            )

            mock_generate_token_cookie.assert_called_once_with(
                auth_service.response, auth_service.redis, str(client_id), str(mock_user.id)
            )

            assert result == mock_profile
