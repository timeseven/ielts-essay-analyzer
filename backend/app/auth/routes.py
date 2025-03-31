from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from app.schemas import CustomResponse

# Auth
from app.auth.services import generate_token_cookie

# Core
from app.db.deps import WriteDbDep, SimpleDbDep

# from app.users.deps import UserDep
from app.auth.deps import AccessDep

# Users
from app.user.schemas import UserCreate, ProfileOut

from app.user.services import create_user

auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=CustomResponse
)
async def register(
    db: WriteDbDep,
    response: ORJSONResponse,
    form_data: UserCreate,
) -> ProfileOut:
    client_id = form_data.client_id

    # Create user
    user = await create_user(
        db, form_data.username, form_data.email, form_data.password
    )


#     """
#     Registers a new user.

#     This endpoint allows clients to create a new user account by providing a username,
#     email, and password. Upon successful registration, a user object is returned and
#     an authentication token is generated and set as an HTTP-only cookie.

#     Args:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- db (DbDep): The database connection dependency.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- form_data (UserCreate): The form data containing the username,
#         email, and password.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- response (ORJSONResponse): The HTTP response object.<br>

#     Returns:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 201: Created -> A response containing the created user object and
#         an authentication token in an HTTP-only cookie.

#     Raises:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 400: Bad Request -> User already exists or email already exists.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 422: Unprocessable Content -> Validation error for the form data.<br>

#     """
#     # Create user
#     user = await create_user(
#         db, form_data.username, form_data.email, form_data.password
#     )

#     # Generate token and set cookies
#     await generate_token_cookie(db, str(user.get("id")), response)

#     return User(**user).model_dump()


# @auth_router.post(
#     "/login",
# )
# async def login(
#     write_db: WriteDbDep,
#     simple_db: SimpleDbDep,
#     form_data: UserLogin,
#     response: ORJSONResponse,
# ) -> User:
#     """
#     Logins a user

#     This endpoint allows clients to log in a user by providing a username(email) and password.
#     If the user is authenticated, an authentication token is generated and set as an
#     HTTP-only cookie.

#     Args:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- db (DbDep): The database connection dependency.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- form_data (UserCreate): The form data containing the username(email) and password.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- response (ORJSONResponse): The HTTP response object.<br>

#     Returns:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 200: OK -> A response containing the authenticated user object and an authentication
#         token in an HTTP-only cookie.

#     Raises:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 401: Unauthorized -> Incorrect username or password.<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 422: Unprocessable Content -> Validation error for the form data.<br>
#     """
#     # Validate user
#     user = await authenticate_user(simple_db, form_data.username, form_data.password)

#     # Generate token and set cookies
#     await generate_token_cookie(write_db, str(user.get("id")), response)

#     return User(**user).model_dump()


# @auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
# async def logout(response: ORJSONResponse):
#     """
#     Logs out a user

#     This endpoint allows clients to log out a user by clearing the authentication token
#     cookie.

#     Args:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp;- response (ORJSONResponse): The HTTP response object.<br>

#     Returns:<br>
#         &nbsp;&nbsp;&nbsp;&nbsp; 204: No Content -> User logged out successfully.<br>
#     """
#     # Clear cookies
#     response.delete_cookie("access_token")
#     response.delete_cookie("jti")


# @auth_router.put("/reset-password")
# async def reset_password(user: UserDep):
#     pass
