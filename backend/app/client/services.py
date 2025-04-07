from databases import Database
from databases.backends.postgres import Record

from app.client.exceptions import ClientBadRequest


class ClientService:
    def __init__(self, db: Database):
        self.db = db

    async def create_client(self, name: str) -> Record:
        query = """INSERT INTO clients (name) VALUES (:name) RETURNING *"""
        try:
            created_user = await self.db.fetch_one(
                query=query,
                values={
                    "name": name,
                },
            )
            return created_user
        except Exception as e:
            raise ClientBadRequest(detail=f"Failed to create user: {str(e)}")

    async def assign_client_owner(self, client_id: str, owner_id: str):
        query = """UPDATE clients SET owner_id = :owner_id WHERE id = :client_id"""
        try:
            values = {
                "client_id": client_id,
                "owner_id": owner_id,
            }
            await self.db.execute(query=query, values=values)
        except Exception as e:
            raise ClientBadRequest(detail=f"Failed to create user: {str(e)}")
