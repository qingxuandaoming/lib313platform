from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/lab313_platform"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload
    UPLOAD_DIR: str = "../uploads"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    # Admin bootstrap
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
