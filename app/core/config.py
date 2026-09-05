from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "CloudVault"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # Database (SQLite for local, PostgreSQL for prod)
    DATABASE_URL: str = "sqlite:///./cloudvault.db"

    # Auth
    SECRET_KEY: str = "CHANGE-ME-USE-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "cloudvault-bucket"
    S3_PRESIGNED_URL_EXPIRY: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
