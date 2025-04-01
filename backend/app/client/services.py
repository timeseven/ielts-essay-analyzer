from databases.backends.postgres import Record
from databases import Database
from pydantic import EmailStr

from app.client.exceptions import ClientBadRequest


async def create_client(db: Database, name: str, owner_id: str | None = None) -> Record:
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


async def assign_client_owner(db: Database, client_id: str, owner_id: str):
    query = (
        """UPDATE clients SET owner_id = :owner_id WHERE id = :client_id RETURNING *"""
    )
    try:
        values = {
            "client_id": client_id,
            "owner_id": owner_id,
        }
        await db.execute(query=query, values=values)
    except Exception as e:
        raise ClientBadRequest(detail=f"Failed to create user: {str(e)}")
