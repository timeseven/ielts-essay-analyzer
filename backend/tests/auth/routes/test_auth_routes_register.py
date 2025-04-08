from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_register_route():
    mock_profile = {
        "user_id": "d9b552bd-164e-4fbb-868b-2855e1a51136",
        "client_id": "0c04f5d3-30b8-4a9f-a330-b9b5b7427149",
        "full_name": "Test User",
        "status": "active",
        "is_client_owner": True,
    }

    with patch("app.auth.routes.AuthService", autospec=True) as MockAuthService:
        auth_service_instance = MockAuthService.return_value
        auth_service_instance.register = AsyncMock(return_value=mock_profile)

        async with AsyncClient(base_url="http://test/") as client:
            user_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "securepassword",
                "client_name": "Test Client",
                "client_id": None,
            }

            response = await client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
            print("response", response)
            assert response.status_code == status.HTTP_201_CREATED
            # response_data = response.json()
            # assert response_data["code"] == status.HTTP_201_CREATED
            # assert response_data["message"] == "User created successfully"
            # assert response_data["data"] == mock_profile

            # auth_service_instance.register.assert_called_once_with(
            #     username=user_data["username"],
            #     email=user_data["email"],
            #     password=user_data["password"],
            #     client_name=user_data["client_name"],
            #     client_id=user_data["client_id"],
            # )
