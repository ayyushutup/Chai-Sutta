"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Chai Sutta application settings loaded from environment variables."""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False,
    )

    # Database
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/chaisutta'
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = 'redis://localhost:6379/0'

    # JWT
    JWT_SECRET_KEY: str = 'change-me-in-production'
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''

    # LLM
    GEMINI_API_KEY: str = ''
    GROQ_API_KEY: str = ''

    # Twitter (burner)
    TWITTER_USERNAME: str = ''
    TWITTER_EMAIL: str = ''
    TWITTER_PASSWORD: str = ''

    # Reddit
    REDDIT_CLIENT_ID: str = ''
    REDDIT_CLIENT_SECRET: str = ''
    REDDIT_USER_AGENT: str = 'chai-sutta:v1.0'

    # TomTom
    TOMTOM_API_KEY: str = ''

    # Storage
    STORAGE_BACKEND: str = 'local'
    LOCAL_STORAGE_PATH: str = './uploads'

    # Qdrant
    QDRANT_HOST: str = 'localhost'
    QDRANT_PORT: int = 6333

    # App
    APP_ENV: str = 'development'
    APP_DEBUG: bool = True
    APP_HOST: str = '0.0.0.0'
    APP_PORT: int = 8000


settings = Settings()
