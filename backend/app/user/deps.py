import jwt
from fastapi import Depends
from typing import Annotated
from databases import Database
from jwt.exceptions import InvalidTokenError
from databases.backends.postgres import Record

# Config
from app.auth.config import auth_settings

# Deps
from app.db.deps import SimpleDbDep
from app.auth.deps import AccessDep


# Exceptions
from app.user.exceptions import UserNotAuthenticated


async def get_profile_by_id(db: Database, client_id: str, user_id: str):
    query = "SELECT * FROM profiles WHERE client_id = :client_id AND user_id = :user_id"
    return await db.fetch_one(
        query=query, values={"client_id": client_id, "user_id": user_id}
    )


async def get_current_profile(db: SimpleDbDep, token: AccessDep, client_id: str):
    try:
        access_token = token.get("access_token")
        payload = jwt.decode(
            access_token,
            auth_settings.ACCESS_SECRET_KEY,
            algorithms=[auth_settings.ALGORITHM],
        )
        payload_client_id = payload.get("client_id")
        payload_user_id = payload.get("user_id")
    except InvalidTokenError as e:
        raise UserNotAuthenticated
    if payload_client_id != client_id:
        raise UserNotAuthenticated
    profile = await get_profile_by_id(db, payload_client_id, payload_user_id)
    if profile is None:
        raise UserNotAuthenticated
    return profile


ProfileDep = Annotated[Record, Depends(get_current_profile)]
