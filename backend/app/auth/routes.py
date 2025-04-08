from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from app.auth.services import AuthService
from app.auth.swagger import login_responses, register_responses
from app.db.deps import RedisDep, WriteDbDep
from app.schemas import CustomResponse
from app.user.schemas import ProfileOut, UserCreate, UserLogin

auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomResponse[ProfileOut],
    responses=register_responses,
)
async def register(
    db: WriteDbDep,
    redis: RedisDep,
    response: ORJSONResponse,
    form_data: UserCreate,
) -> CustomResponse[ProfileOut]:
    """
    Registers a new user and creates an associated profile.

    This endpoint is responsible for registering a new user by creating a user
    profile in the database. It accepts user credentials and client information,
    and returns a custom response with the user's profile data upon successful
    registration.

    Args:
        db (WriteDbDep): Database dependency for executing database operations.
        redis (RedisDep): Redis dependency for caching and session management.
        response (ORJSONResponse): FastAPI response object for setting response data.
        form_data (UserCreate): Data required to create a new user, including
            username, email, password, client name, and client ID.

    Returns:
        CustomResponse[ProfileOut]: A custom response containing the newly created
        user's profile information.

    Responses:
        201: User created successfully with profile details.
        422: Validation errors if the input data does not meet specified criteria.
    """
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
    responses=login_responses,
)
async def login(
    db: WriteDbDep,
    redis: RedisDep,
    response: ORJSONResponse,
    form_data: UserLogin,
) -> CustomResponse[ProfileOut]:
    """
    Logs in a user and returns the user's profile information.

    This endpoint is responsible for authenticating a user and returning the user's
    profile information upon successful login.

    Args:
        db (WriteDbDep): Database dependency for executing database operations.
        redis (RedisDep): Redis dependency for caching and session management.
        response (ORJSONResponse): FastAPI response object for setting response data.
        form_data (UserLogin): Data required to login a user, including
            username and password.

    Returns:
        CustomResponse[ProfileOut]: A custom response containing the logged in
        user's profile information.

    Responses:
        200: User logged in successfully with profile details.
        422: Validation errors if the input data does not meet specified criteria.
    """
    auth_service = AuthService(db, redis, response)

    profile = await auth_service.login(username=form_data.username, password=form_data.password)

    return CustomResponse(
        code=status.HTTP_200_OK,
        message="User logged in successfully",
        data=profile,
    )
