import os
from typing import Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/tododb"

    # JWT Configuration
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"

    # Application
    DEBUG: bool = False
    APP_NAME: str = "Phase III Todo API"
    APP_VERSION: str = "0.1.0"

    # CORS - comma-separated string that will be parsed
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Better Auth
    BETTER_AUTH_SECRET: str = ""
    BETTER_AUTH_URL: str = ""

    @property
    def parsed_allowed_origins(self) -> list[str]:
        """Parse ALLOWED_ORIGINS from comma-separated string."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
