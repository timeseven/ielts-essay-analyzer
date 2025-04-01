from app.config import BaseSettings


class AuthConfig(BaseSettings):
    ALGORITHM: str = "HS256"
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 mins
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 2  # 2 days


auth_settings = AuthConfig()
