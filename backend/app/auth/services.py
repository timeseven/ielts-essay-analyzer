from uuid import UUID

from databases import Database
from databases.backends.postgres import Record
from fastapi.responses import ORJSONResponse
from pydantic import EmailStr
from redis.asyncio import Redis

from app.auth.utils import generate_token_cookie
from app.client.services import ClientService
from app.user.services import UserService
from app.user.utils import authenticate_user


class AuthService:
    def __init__(self, db: Database, redis: Redis, response: ORJSONResponse):
        """
        Initialize the AuthService with database, Redis, and response dependencies.

        Args:
            db (Database): The database connection used for user and client operations.
            redis (Redis): The Redis connection used for token management.
            response (ORJSONResponse): The ORJSON response object used to set cookies.
        """
        self.db = db
        self.redis = redis
        self.response = response

    async def register(
        self,
        username: str,
        email: EmailStr,
        password: str,
        client_name: str | None,
        client_id: UUID | None,
    ) -> Record:
        """
        Registers a new user, potentially creating a new client if no client ID is provided.

        This method handles the registration process by creating a new user and, if necessary,
        a new client. It updates the user's current client ID, creates a user profile, and
        generates a token to set in cookies.

        Args:
            username (str): The username for the new user.
            email (EmailStr): The email address for the new user.
            password (str): The password for the new user.
            client_name (str | None): The name of the client to create if no client ID is provided.
            client_id (UUID | None): The client ID to associate with the user, if available.

        Returns:
            Record: The newly created user profile record.
        """
        user_service = UserService(self.db)

        # Create user
        user = await user_service.create_user(
            username=username,
            email=email,
            password=password,
        )

        client_service = ClientService(self.db)

        if client_id is None:
            # Create client
            client = await client_service.create_client(name=client_name)
            client_id = client.id

        # Set client id to user current_client_id
        await user_service.update_user_current_client(user.id, client_id)

        # Create profile
        profile = await user_service.create_profile(
            client_id=client_id,
            user_id=user.id,
            full_name=user.username,
            is_client_owner=True,
        )

        # Generate token and set cookies
        await generate_token_cookie(
            self.response,
            self.redis,
            str(client_id),
            str(user.id),
        )

        return profile

    async def login(self, username: str, password: str) -> Record:
        """
        Login a user and return the updated profile record.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            Record: The updated user profile record.
        """
        user_service = UserService(self.db)

        # Validate user
        user = await authenticate_user(self.db, username, password)

        # Update profile
        profile = await user_service.update_profile_login(user.current_client_id, user.id)

        # Generate token and set cookies
        await generate_token_cookie(
            self.response,
            self.redis,
            str(user.current_client_id),
            str(user.id),
        )

        return profile
