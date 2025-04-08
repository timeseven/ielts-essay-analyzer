from fastapi import status

from app.utils import response_model

register_responses = {
    status.HTTP_201_CREATED: response_model(
        "Successful Response",
        status.HTTP_201_CREATED,
        "User created successfully",
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "5fa85f64-5717-4562-b3fc-2c963f66afa2",
            "status": "active",
            "full_name": "test user",
            "avatar_url": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50",
            "last_login_at": "2025-04-01T02:20:54.822654Z",
            "created_at": "2025-04-01T02:20:54.822654",
            "updated_at": "2025-04-01T02:20:54.822654",
        },
    ),
    status.HTTP_422_UNPROCESSABLE_ENTITY: response_model(
        "Validation Error",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        [
            {"password": "Password must be at least 8 characters long"},
            {"username": "Username must be at least 3 characters long"},
        ],
        None,
    ),
}


login_responses = {
    status.HTTP_200_OK: response_model(
        "Successful Response",
        status.HTTP_200_OK,
        "User logged in successfully",
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_id": "5fa85f64-5717-4562-b3fc-2c963f66afa2",
            "status": "active",
            "full_name": "test user",
            "avatar_url": "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50",
            "last_login_at": "2025-04-01T02:20:54.822654Z",
            "created_at": "2025-04-01T02:20:54.822654",
            "updated_at": "2025-04-01T02:20:54.822654",
        },
    ),
    status.HTTP_422_UNPROCESSABLE_ENTITY: response_model(
        "Validation Error",
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        [
            {"password": "Password must be at least 8 characters long"},
            {"username": "Username must be at least 3 characters long"},
        ],
        None,
    ),
}
