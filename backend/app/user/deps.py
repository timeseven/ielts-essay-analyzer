from typing import Annotated

import jwt
from databases import Database
from databases.backends.postgres import Record
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from app.auth.config import auth_settings
from app.auth.deps import AccessDep
from app.db.deps import SimpleDbDep
from app.user.exceptions import UserNotAuthenticated


async def get_profile_by_id(db: Database, client_id: str, user_id: str):
    """
    Fetches a profile record from the database using the given client_id and user_id.

    Args:
        db (Database): The database connection.
        client_id (str): The client_id of the profile.
        user_id (str): The user_id of the profile.

    Returns:
        Record: The fetched profile record.
    """
    query = "SELECT * FROM profiles WHERE client_id = :client_id AND user_id = :user_id"
    return await db.fetch_one(query=query, values={"client_id": client_id, "user_id": user_id})


async def get_current_profile(db: SimpleDbDep, token: AccessDep, client_id: str):
    """
    Retrieve the current user's profile from the database.

    This function decodes the provided access token to extract the client_id
    and user_id, then fetches the corresponding profile from the database.
    If the token is invalid, or if the client_id does not match, it raises
    a UserNotAuthenticated exception.

    Args:
        db (SimpleDbDep): The database dependency for executing queries.
        token (AccessDep): The access token dependency containing the JWT.
        client_id (str): The expected client_id to validate against the token.

    Returns:
        Record: The user's profile record from the database.

    Raises:
        UserNotAuthenticated: If the token is invalid, the client_id does not match,
        or the profile does not exist.
    """

    try:
        access_token = token.get("access_token")
        payload = jwt.decode(
            access_token,
            auth_settings.ACCESS_SECRET_KEY,
            algorithms=[auth_settings.ALGORITHM],
        )
        payload_client_id = payload.get("client_id")
        payload_user_id = payload.get("user_id")
    except InvalidTokenError:
        raise UserNotAuthenticated
    if payload_client_id != client_id:
        raise UserNotAuthenticated
    profile = await get_profile_by_id(db, payload_client_id, payload_user_id)
    if profile is None:
        raise UserNotAuthenticated
    return profile


ProfileDep = Annotated[Record, Depends(get_current_profile)]
