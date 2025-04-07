from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

# Dependencies
from app.db.deps import WriteDbDep, RedisDep

# Schemas
from app.schemas import CustomResponse
from app.user.schemas import UserCreate, UserLogin, ProfileOut

# Services
from app.auth.services import AuthService

# Utils
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
    auth_service = AuthService(db, redis, response)

    profile = await auth_service.register(
        username=form_data.username,
        email=form_data.email,
        password=form_data.password,
        client_name=form_data.client_name,
        client_id=form_data.client_id,
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
    response: ORJSONResponse,
    form_data: UserLogin,
) -> CustomResponse[ProfileOut]:
    auth_service = AuthService(db, redis, response)

    profile = await auth_service.login(
        username=form_data.username, password=form_data.password
    )

    return CustomResponse(
        code=status.HTTP_200_OK,
        message="User logged in successfully",
        data=profile,
    )
