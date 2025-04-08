from databases import Database
from databases.backends.postgres import Record
from pydantic import EmailStr

from app.auth.utils import verify_password
from app.user.exceptions import UserBadRequest, UserNotAuthenticated


async def authenticate_user(db: Database, username: str, password: str) -> Record | None:
    """
    Authenticates a user by verifying their username and password.

    Args:
        db (Database): The database connection used to retrieve user data.
        username (str): The username or email of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        Record | None: The user record if authenticated, or raises UserNotAuthenticated if authentication fails.

    Raises:
        UserNotAuthenticated: If the username does not exist or the password is incorrect.
    """

    from app.user.services import UserService

    user_service = UserService(db)
    user = await user_service.get_user(username)
    if user is None or not verify_password(password, user.hashed_password):
        raise UserNotAuthenticated(detail="Incorrect username or password")
    return user


async def check_users_field_exists(db: Database, field: str, value: str, user: Record | None = None) -> bool:
    """
    Checks if a specified field with a given value exists in the users table,
    excluding a particular user record if provided.

    Args:
        db (Database): The database connection used to query the users table.
        field (str): The name of the field to check for existence.
        value (str): The value to check for existence in the specified field.
        user (Record | None): An optional user record to exclude from the check.

    Returns:
        bool: True if the field with the specified value exists in the users table,
        otherwise False.
    """

    if user and user.get(field) == value:
        return False

    query = f"SELECT * FROM users WHERE {field} = :{field}"
    existing_field = await db.fetch_one(query=query, values={field: value})

    return existing_field


async def check_username_email_exists(db: Database, username: str, email: EmailStr, user: Record | None = None) -> dict:
    """
    Checks if the provided username or email already exists in the users table,
    excluding a particular user record if provided. Raises an exception if either
    the username or email already exists.

    Args:
        db (Database): The database connection used to query the users table.
        username (str): The username to check for existence.
        email (EmailStr): The email address to check for existence.
        user (Record | None): An optional user record to exclude from the check.

    Returns:
        dict: A dictionary containing error messages for the fields that already exist.

    Raises:
        UserBadRequest: If the username or email already exists in the users table.
    """

    errors = []

    # Check for username and email existence
    if await check_users_field_exists(db, "username", username, user):
        errors.append({"username": "Username already exists."})
    if await check_users_field_exists(db, "email", email, user):
        errors.append({"email": "Email already exists."})

    if errors:
        raise UserBadRequest(detail=errors)
