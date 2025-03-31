from asyncpg import Record
from databases import Database
from pydantic import EmailStr
from uuid import UUID

from app.client.exceptions import ClientBadRequest


async def create_client(
    db: Database, name: str, owner_id: UUID | None = None
) -> Record:
    query = (
        """INSERT INTO clients (name, owner_id) VALUES (:name, :owner_id) RETURNING *"""
    )

    try:
        values = {
            "name": name,
            "owner_id": owner_id,
        }
        created_user = await db.fetch_one(query=query, values=values)
        return created_user
    except Exception as e:
        raise ClientBadRequest(detail=f"Failed to create user: {str(e)}")
