from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from app.schemas import CustomResponse

# Auth
from app.auth.services import generate_token_cookie

# Core
from app.db.deps import WriteDbDep, RedisDep

# from app.users.deps import UserDep
from app.auth.deps import AccessDep

# Users
from app.user.schemas import UserCreate, UserLogin, ProfileOut

from app.user.services import (
    create_user,
    create_profile,
    authenticate_user,
    update_profile_login,
    update_user_current_client,
)

from app.client.services import assign_client_owner, create_client

from app.utils import response_model

auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomResponse[ProfileOut],
    responses={
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
    },
)
async def register(
    db: WriteDbDep,
    redis: RedisDep,
    response: ORJSONResponse,
    form_data: UserCreate,
) -> CustomResponse[ProfileOut]:
    client_id = form_data.client_id

    # Create user
    user = await create_user(
        db, form_data.username, form_data.email, form_data.password
    )
    # If client id is provided, our app will generate a client when user starts using the app. Registration is needed when user
    # runs out of 10 times of free trial.
    if client_id:
        # Assign user to client as owner
        await assign_client_owner(db, client_id, user.id)
    else:
        # Create a new client for the user
        client = await create_client(db, form_data.client_name, user.id)
        client_id = client.id

    # Set client id to user current_client_id
    await update_user_current_client(db, user.id, client_id)

    # Create user profile
    profile = await create_profile(db, client_id, user.id, user.username)

    # Generate token and set cookies
    await generate_token_cookie(
        response,
        redis,
        str(client_id),
        str(user.id),
    )

    return CustomResponse(
        code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=profile,
    )


@auth_router.post(
    "/login",
    response_model=CustomResponse[ProfileOut],
)
async def login(
    db: WriteDbDep,
    redis: RedisDep,
    form_data: UserLogin,
    response: ORJSONResponse,
) -> CustomResponse[ProfileOut]:
    # Validate user
    user = await authenticate_user(db, form_data.username, form_data.password)

    # Update profile
    profile = await update_profile_login(db, user.current_client_id, user.id)

    # Generate token and set cookies
    await generate_token_cookie(
        response,
        redis,
        str(user.current_client_id),
        str(user.id),
    )

    return CustomResponse(
        code=status.HTTP_200_OK,
        message="User logged in successfully",
        data=profile,
    )
