from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "Metadata UI API"
    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/metadata_ui"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings=Settings()
