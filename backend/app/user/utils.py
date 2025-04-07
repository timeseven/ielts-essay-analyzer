from pydantic import EmailStr
from databases import Database
from databases.backends.postgres import Record


from app.user.exceptions import UserBadRequest, UserNotAuthenticated
from app.auth.utils import verify_password


async def authenticate_user(
    db: Database, username: str, password: str
) -> Record | None:
    from app.user.services import UserService

    user_service = UserService(db)
    user = await user_service.get_user(username)
    if user is None or not verify_password(password, user.hashed_password):
        raise UserNotAuthenticated(detail="Incorrect username or password")
    return user


# Checks if field of a user exists
async def check_users_field_exists(
    db: Database, field: str, value: str, user: Record | None = None
) -> bool:
    if user and user.get(field) == value:
        return False

    query = f"SELECT * FROM users WHERE {field} = :{field}"
    existing_field = await db.fetch_one(query=query, values={field: value})

    return existing_field


# Checks if username or email already exists
async def check_username_email_exists(
    db: Database, username: str, email: EmailStr, user: Record | None = None
) -> dict:
    errors = []

    # Check for username and email existence
    if await check_users_field_exists(db, "username", username, user):
        errors.append({"username": "Username already exists."})
    if await check_users_field_exists(db, "email", email, user):
        errors.append({"email": "Email already exists."})

    if errors:
        raise UserBadRequest(detail=errors)
