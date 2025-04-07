from uuid import UUID
from pydantic import EmailStr
from databases import Database
from redis.asyncio import Redis
from fastapi.responses import ORJSONResponse
from databases.backends.postgres import Record

# Services
from app.user.services import UserService
from app.client.services import ClientService

# Utils
from app.auth.utils import generate_token_cookie
from app.user.utils import authenticate_user


class AuthService:
    def __init__(self, db: Database, redis: Redis, response: ORJSONResponse):
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
        user_service = UserService(self.db)

        # Validate user
        user = await authenticate_user(self.db, username, password)

        # Update profile
        profile = await user_service.update_profile_login(
            user.current_client_id, user.id
        )

        # Generate token and set cookies
        await generate_token_cookie(
            self.response,
            self.redis,
            str(user.current_client_id),
            str(user.id),
        )

        return profile
