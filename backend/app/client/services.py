from databases import Database
from databases.backends.postgres import Record

from app.client.exceptions import ClientBadRequest


class ClientService:
    def __init__(self, db: Database):
        self.db = db

    async def create_client(self, name: str) -> Record:
        """
        Creates a new client in the database with the specified name.

        This method inserts a new record into the clients table using the provided
        client name and returns the created client record.

        Args:
            name (str): The name of the client to be created.

        Returns:
            Record: The newly created client record.

        Raises:
            ClientBadRequest: If the client creation fails due to a database error.
        """

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
        """
        Assigns the specified owner to the specified client.

        This method updates the specified client by setting its owner_id to the
        specified owner_id.

        Args:
            client_id (str): The ID of the client to be updated.
            owner_id (str): The ID of the owner to be assigned to the client.

        Raises:
            ClientBadRequest: If the assignment fails due to a database error.
        """
        query = """UPDATE clients SET owner_id = :owner_id WHERE id = :client_id"""
        try:
            values = {
                "client_id": client_id,
                "owner_id": owner_id,
            }
            await self.db.execute(query=query, values=values)
        except Exception as e:
            raise ClientBadRequest(detail=f"Failed to create user: {str(e)}")
