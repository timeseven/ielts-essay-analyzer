from asyncpg import Record
from databases import Database
from pydantic import EmailStr

from app.user.exceptions import UserBadRequest

from app.auth.utils import get_password_hash


# Retrieves the user by username or email
async def get_user(db: Database, username: str) -> Record:
    query = "SELECT * FROM users WHERE username = :username OR email = :username"
    return await db.fetch_one(query=query, values={"username": username})


# Checks if field of a user exists
async def check_field_exists(
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
    if await check_field_exists(db, "username", username, user):
        errors.append({"username": "Username already exists."})
    if await check_field_exists(db, "email", email, user):
        errors.append({"email": "Email already exists."})

    if errors:
        raise UserBadRequest(detail=errors)


async def create_user(
    db: Database,
    username: str,
    email: EmailStr,
    password: str,
    is_admin: bool | None = False,
) -> Record:
    await check_username_email_exists(db, username, email)

    query = """INSERT INTO users (username, email, hashed_password, is_admin)
             VALUES (:username, :email, :hashed_password, :is_admin) RETURNING *"""

    try:
        hashed_password = get_password_hash(password)
        values = {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "is_admin": is_admin,
        }
        created_user = await db.fetch_one(query=query, values=values)
        return created_user
    except Exception as e:
        raise UserBadRequest(detail=f"Failed to create user: {str(e)}")
