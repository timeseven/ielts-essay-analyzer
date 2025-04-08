from databases import Database
from databases.backends.postgres import Record
from pydantic import EmailStr

from app.auth.utils import get_password_hash, verify_password
from app.user.exceptions import UserBadRequest, UserNotAuthenticated
from app.user.utils import check_username_email_exists


class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def get_user(self, username: str) -> Record:
        """
        Retrieves a user by username or email.

        Args:
            username (str): The username or email of the user to retrieve.

        Returns:
            Record: The user record if found, otherwise None.
        """
        query = "SELECT * FROM users WHERE username = :username OR email = :username"
        return await self.db.fetch_one(query=query, values={"username": username})

    async def authenticate_user(self, username: str, password: str) -> Record:
        """
        Authenticates a user by verifying their username and password.

        Args:
            username (str): The username or email of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            Record: The user record if authenticated, otherwise raises UserNotAuthenticated.

        Raises:
            UserNotAuthenticated: If the username or password is invalid.
        """
        user = await self.get_user(username)
        if user is None or not verify_password(password, user.hashed_password):
            raise UserNotAuthenticated(detail="Incorrect username or password")
        return user

    async def check_users_field_exists(self, field: str, value: str, user: Record | None = None) -> bool:
        """
        Checks if a given field exists in the users table.

        Args:
            field (str): The field to check for existence.
            value (str): The value of the field to check.
            user (Record | None): The user record to exclude from the check.

        Returns:
            bool: True if the field exists, otherwise False.
        """
        if user and user.get(field) == value:
            return False

        query = f"SELECT * FROM users WHERE {field} = :{field}"
        existing_field = await self.db.fetch_one(query=query, values={field: value})

        return existing_field

    async def create_user(
        self,
        username: str,
        email: EmailStr,
        password: str,
        is_admin: bool | None = False,
    ) -> Record:
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the new user.
            email (EmailStr): The email address of the new user.
            password (str): The password of the new user.
            is_admin (bool | None): Whether the user is an admin or not.

        Returns:
            Record: The created user record.

        Raises:
            UserBadRequest: If the user could not be created due to a bad request.
        """
        await check_username_email_exists(self.db, username, email)

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
            created_user = await self.db.fetch_one(query=query, values=values)
            return created_user
        except Exception as e:
            raise UserBadRequest(detail=f"Failed to create user: {str(e)}")

    async def update_user_current_client(self, user_id: str, client_id: str):
        """
        Updates a user's current_client_id in the database.

        Args:
            user_id (str): The id of the user to update.
            client_id (str): The id of the client to set as the user's current client.

        Raises:
            UserBadRequest: If the client could not be updated due to a bad request.
        """

        query = """UPDATE users SET current_client_id = :client_id WHERE id = :user_id"""
        try:
            values = {
                "user_id": user_id,
                "client_id": client_id,
            }
            await self.db.execute(query=query, values=values)
        except Exception as e:
            raise UserBadRequest(detail=f"Failed to update current client: {str(e)}")

    async def create_profile(
        self,
        client_id: str,
        user_id: str,
        full_name: str,
        is_client_owner: bool = False,
    ) -> Record:
        """
        Creates a new profile in the database for a user with the specified client ID.

        This method inserts a new record into the profiles table with the given client ID,
        user ID, full name, and ownership status. It sets the profile's status to active
        and records the current timestamp as the last login time.

        Args:
            client_id (str): The ID of the client associated with the profile.
            user_id (str): The ID of the user associated with the profile.
            full_name (str): The full name of the user.
            is_client_owner (bool, optional): Indicates if the user is the client owner. Defaults to False.

        Returns:
            Record: The newly created profile record.

        Raises:
            UserBadRequest: If the profile creation fails due to a database error.
        """

        query = """INSERT INTO profiles (client_id, user_id, full_name, is_client_owner, last_login_at, status) VALUES
        (:client_id, :user_id,:full_name, :is_client_owner, NOW(), 'active') RETURNING *"""
        try:
            values = {
                "client_id": client_id,
                "user_id": user_id,
                "full_name": full_name,
                "is_client_owner": is_client_owner,
            }
            return await self.db.fetch_one(query=query, values=values)
        except Exception as e:
            raise UserBadRequest(detail=f"Failed to create user: {str(e)}")

    async def update_profile_login(self, client_id: str, user_id: str):
        """
        Updates the last login time for a profile with the specified client ID and user ID.

        Args:
            client_id (str): The ID of the client associated with the profile.
            user_id (str): The ID of the user associated with the profile.

        Returns:
            Record: The updated profile record.

        Raises:
            UserBadRequest: If the profile update fails due to a database error.
        """
        query = """UPDATE profiles SET last_login_at = NOW() WHERE client_id = :client_id AND
        user_id = :user_id RETURNING *"""
        try:
            values = {
                "client_id": client_id,
                "user_id": user_id,
            }
            return await self.db.fetch_one(query=query, values=values)
        except Exception as e:
            raise UserBadRequest(detail=f"Failed to update profile login: {str(e)}")
